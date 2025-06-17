from django.contrib import admin
from .models import Order, OrderItem, Product, Category, Customer

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity')
    can_delete = False
    extra = 0
    max_num = 0

    def has_add_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'total_price', 'date_ordered', 'payment_method')
    readonly_fields = ('first_name', 'last_name', 'country', 'address', 'city', 'postal_code', 'payment_method', 'date_ordered', 'total_price', 'state', 'order_id')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)