from django.contrib import admin
from .models import userInfo,UserAddress,Cart,CartItems,Product,SellerProfile,Order,OrderItems

@admin.register(userInfo)
class userInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_email', 'otp', 'is_verified')
    search_fields = ('user__username', 'user__email')

    def get_username(self, obj):
        return obj.user.username if obj.user else "-"
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email if obj.user else "-"
    get_email.short_description = 'Email'
    
admin.site.register(UserAddress)
admin.site.register(Cart)
admin.site.register(CartItems)

admin.site.register(SellerProfile)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
        list_display = ['title','description','price']
        
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
        list_display = ['user','product','amount','razorpay_order_id','']


@admin.register(OrderItems)
class OrderItemAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderItems
        list_display = [field.name for field in OrderItems._meta.get_fields()]
