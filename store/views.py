from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem, Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import stripe
import json
import requests
from decimal import Decimal
import logging
import uuid
from django.core.cache import cache
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse, HttpResponseBadRequest
logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse("Welcome to Essential Threads Backend!")


class ProductList(APIView):
    def get(self, request):
        category = request.query_params.get('category') 
        products = Product.objects.all()
        
        if category:
            products = products.filter(category__name__iexact=category)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


stripe.api_key = settings.STRIPE_SECRET_KEY



def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html' )


def save_data(first_name, last_name, country, state, address, city, postal_code, payment_method, total_price, items, order_id):
    print("save_data called")
    order = Order.objects.create(
        order_id=order_id,
        first_name=first_name,
        last_name=last_name,
        country=country,
        state=state,
        address=address,
        city=city,
        postal_code=postal_code,
        payment_method=payment_method,
        date_ordered=now(),
        total_price=total_price
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(product=product, quantity=item['quantity'], order=order)

@csrf_exempt
def submit_order(request):
    order_id = str(uuid.uuid4()) 
    print("submit_order reached")
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        country = data.get('country')
        state = data.get('state')
        address = data.get('address')
        city = data.get('city')
        postal_code = data.get('postal_code')
        payment_method = data.get('payment_method')
        items = data.get('cart', [])
        total_price = Decimal(data.get('total', 0))

        if payment_method == "Cash":
            save_data(first_name, last_name, country, state, address, city, postal_code, "Cash", total_price, items, order_id)
            return JsonResponse({'redirect_url': '/api/success'}, status=201)

        elif payment_method == "Credit Card":
            cache.set(order_id, {
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'state': state,
                'address': address,
                'city': city,
                'postal_code': postal_code,
                'total_price': str(total_price),
                'items': items,
                'payment_method': 'Credit Card',
            }, timeout=60*15)

            line_items = []
            for item in items:
                product = Product.objects.get(id=item['id'])
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': product.name},
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': item['quantity'],
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://essentialthreads-backend.onrender.com/api/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://essentialthreads-backend.onrender.com/api/cancel/',
                metadata={
                    'order_id': order_id,
                }
            )

            return JsonResponse({'sessionId': session.id, 'checkout_url': session.url}, status=200)

        elif payment_method == "PayPal":
            print("paypal called")
            auth = requests.post(
                "https://api-m.sandbox.paypal.com/v1/oauth2/token",
                auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                headers={"Accept": "application/json"},
                data={"grant_type": "client_credentials"},
            )
            if auth.status_code != 200:
                return JsonResponse({'error': 'PayPal authentication failed'}, status=500)

            access_token = auth.json().get("access_token")
            if not access_token:
                return JsonResponse({'error': 'Failed to get PayPal access token'}, status=500)

            order_data = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD",
                        "value": str(total_price)
                    },
                    "custom_id": order_id
                }],
                "application_context": {
                    "return_url": "https://essentialthreads-backend.onrender.com/api/paypal-capture",
                    "cancel_url": "https://essentialthreads-backend.onrender.com/api/cancel/"
                }
            }

            paypal_order = requests.post(
                "https://api-m.sandbox.paypal.com/v2/checkout/orders",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                },
                json=order_data
            )

            if paypal_order.status_code == 201:
                paypal_order_data = paypal_order.json()
                paypal_order_id = paypal_order_data.get("id")

                cache.set(paypal_order_id, {
                    'first_name': first_name,
                    'last_name': last_name,
                    'country': country,
                    'state': state,
                    'address': address,
                    'city': city,
                    'postal_code': postal_code,
                    'total_price': str(total_price),
                    'items': items,
                }, timeout=60*15)

                for link in paypal_order_data["links"]:
                    if link["rel"] == "approve":
                        return JsonResponse({'approval_url': link["href"]}, status=200)

            return JsonResponse({'error': 'Failed to create PayPal order'}, status=500)

        else:
            return JsonResponse({'error': 'Unsupported payment method'}, status=400)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def paypal_capture(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponse("Missing token", status=400)

    auth = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
    )
    if auth.status_code != 200:
        return HttpResponse("PayPal auth failed", status=500)

    access_token = auth.json().get("access_token")
    if not access_token:
        return HttpResponse("Failed to get PayPal access token", status=500)

    capture = requests.post(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{token}/capture",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    if capture.status_code == 201:
        cached_order = cache.get(token)
        if not cached_order:
            return HttpResponse("Order data not found in cache", status=400)

        try:
            save_data(
                first_name=cached_order['first_name'],
                last_name=cached_order['last_name'],
                country=cached_order['country'],
                state=cached_order['state'],
                address=cached_order['address'],
                city=cached_order['city'],
                postal_code=cached_order['postal_code'],
                payment_method="Paypal",
                total_price=Decimal(cached_order['total_price']),
                items=cached_order['items'],
                order_id=token
            )
        except Exception as e:
            return HttpResponse(f"Failed to save order data: {e}", status=500)

        return render(request, 'success.html')

    return HttpResponse("Payment capture failed", status=400)


@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)  # Method Not Allowed

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if sig_header is None:
        return HttpResponseBadRequest("Missing Stripe-Signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")

    # Process the event here
    print(f"Received Stripe event: {event['type']}")

    return HttpResponse(status=200)