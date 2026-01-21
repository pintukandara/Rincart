from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("", views.homepage_view, name="homepage"),
    path("logout/", views.logout_view, name="logout"),
    path("verify/", views.verify_otp, name="verify_otp"),
    path("buy/", views.buy_view, name="buy"),
    path("sell/", views.sell_view, name="sell"),
    path("about/", views.about_view, name="about"),
    path("help/", views.help_view, name="help"),
    path("terms/", views.terms_and_condition, name="terms"),
    path('address/<int:product_id>/', views.address_view, name='address'),
    path("add-to-cart/<int:product_id>/",views.add_to_cart_view, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/",views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_view, name="cart_view"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('seller/', views.seller_create_view, name="create-profile"),
    path('seller_profile/<slug:slug>/', views.Seller_profile_view, name="seller_profile"),
    path('send_message/', views.send_message, name='send_message'),
    path('update_password/', views.update_password, name="update_password"),
    path('reset_password/<uidb64>/<token>/',views.reset_password,name='reset_password'),
    path('search_result/', views.search_result, name= "search_result"),
    path('payments/<int:product_id>/', views.payments_view, name="payments"),
    path('payments_cart/', views.payments_cart_view, name="all-checkout"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("delete-item/<int:product_id>", views.DeleteItemView, name="delete_item"),
    path("edit-item/<int:product_id>", views.EditItemView, name="edit_item"),
    path("order_placed", views.order_placed_view, name="order-placed"),
    path("pay-on-delivery/<int:product_id>", views.pay_on_delivery, name="pay-on-delivery"),
    path('cancel-item/<str:order_id>', views.cancel_item, name= "cancel-item")
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
