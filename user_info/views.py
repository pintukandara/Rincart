from .forms import UserRegistrationForm, OTPForm, ProductForm, AddressForm, SellerProfileForm, PasswordResetForm
from .models import userInfo, Product, Cart, CartItems, SellerProfile, Order, UserAddress, OrderItems
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from .tasks import send_verification_code,password_reset_request,send_message_to_pintu,order_confirmation
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.urls import reverse
import razorpay
import random
import time
import json
import re

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def registration_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            request.session['registration_data'] = form.cleaned_data
            user_email = form.cleaned_data['email']
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()
            request.session['user_email'] = user_email
            send_verification_code.delay(user_email,otp)

            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_info/registration.html', {'form': form})


def verify_otp(request):
    form = OTPForm()  # Initialize the form here

    if request.method == "POST":
        form = OTPForm(request.POST)
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        registration_data = request.session.get('registration_data')

        if user_otp and stored_otp and user_otp == str(stored_otp) and registration_data:
            username = registration_data['username']
            email = registration_data['email']
            password = registration_data['password']

            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.is_active = True
            user.save()

            info = userInfo.objects.create(user=user)
            info.save()

            del request.session['registration_data']
            del request.session['otp']
            del request.session['otp_timestamp']
            del request.session['user_email']

            return redirect('login')
        else:
            form.add_error(None, 'Invalid OTP or session expired.')

    return render(request, 'user_info/verify_otp.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('login')
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "invalid Credentials")
            return redirect('login')
        else:
            login(request, user)
            return redirect('homepage')

    return render(request, "user_info/login.html")


def update_password(request):
    if request.method == "POST":
        get_useremail = request.POST.get('email')
        print(get_useremail)
        # print(get_user)
        try:
            get_user = User.objects.filter(email=get_useremail).first()
        except User.DoesNotExist:
            get_user = None

        if get_user is not None:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(get_user)
            uidb64 = urlsafe_base64_encode(force_bytes(get_user.pk))
            print(f"token:{token} Uid:{uidb64}")
            domain = "http://127.0.0.1:8000/"
            reset_path = f'/reset_password/{uidb64}/{token}/'
            # reset_url = f"https:{domain}{reset_path}"
            reset_url = request.build_absolute_uri(
                reverse('reset_password', kwargs={
                        'uidb64': uidb64, 'token': token})
            )
            print(f"Full Reset URL: {reset_url}")
            password_reset_request.delay(get_useremail,get_user.username,reset_url)

    return render(request, "user_info/update_password.html")


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print("this is uid:", uid)
        print("this is user:", user)
        print("Check token:", default_token_generator.check_token(user, token))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('new_password')
                user.set_password(password)
                user.save()
                messages.success(
                    request, "Password has been successfully updated.")
                return redirect('login')
        else:
            form = PasswordResetForm()  # ✅ show empty form on GET
        return render(request, "user_info/reset_password.html", {"form": form})

    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('update_password')


@login_required
def homepage_view(request):
    return render(request, "user_info/Home.html")


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def buy_view(request):
    products = Product.objects.exclude(posted_by=request.user)

    return render(request, "user_info/Buy.html", {"products": products})


@login_required
def address_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address Saved Successfully")
            return redirect("payments", product_id=product.id)

        else:
            messages.error(request, "Try Again")
            return render(request, "user_info/address.html", {
                "product": product,
                "form": form
            })

    else:
        form = AddressForm()

    return render(request, "user_info/address.html", {
        "product": product,
        "form": form
    })


@login_required(login_url='login')
def sell_view(request):
    my_products = Product.objects.filter(posted_by=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.posted_by = request.user
            form.save()
            return redirect('homepage')
    else:
        form = ProductForm()

    return render(request, "user_info/sell.html", {
        "form": form,
        "my_products": my_products
    })


def DeleteItemView(request, product_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('sell')
        else:
            return redirect('login')


@login_required
def EditItemView(request, product_id):

    product = get_object_or_404(Product, id=product_id, posted_by=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('sell')
    else:
        form = ProductForm(instance=product)
    return render(request, "user_info/sell.html", {"form": form})


@login_required(login_url='login')
def about_view(request):
    return render(request, "user_info/about.html")


@login_required(login_url='login')
def help_view(request):
    return render(request, "user_info/help.html")


@login_required
def add_to_cart_view(request, product_id):
    if request.method == "POST":
        user_info, create = userInfo.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart, create = Cart.objects.get_or_create(user=user_info)
        cart_item, item_created = CartItems.objects.get_or_create(
            cart=cart, product=product)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect("cart_view")


@login_required
def cart_view(request):
    total_price = 0
    try:
        user_info = userInfo.objects.get(user=request.user)
    except userInfo.DoesNotExist:
        user_info = None
    if user_info:
        items = CartItems.objects.filter(cart__user=user_info)
        total_price = sum(item.get_total_price() for item in items)
    else:
        items = []
    return render(request, "user_info/cart.html", {
        "items": items,
        "total_price": total_price
    })


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItems, id=product_id)
        cart_item.delete()
        return redirect('cart_view')
    else:
        return redirect('login')


def product_detail(request, slug):

    identified_product = get_object_or_404(Product, slug=slug)
    return render(request, "user_info/product_detail.html", {
        "identified_product": identified_product,

    })


@login_required
def seller_create_view(request):
    # Get the seller profile created by signals.py
    seller_profile = request.user.seller_profile

    if request.method == "POST":
        form = SellerProfileForm(
            request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = SellerProfileForm(instance=seller_profile)

    return render(request, "user_info/seller_create.html", {"form": form})


def Seller_profile_view(request, slug):
    profile = get_object_or_404(SellerProfile, slug=slug)
    return render(request, "user_info/seller_profile.html", {
        "seller_profile": profile

    })


def send_message(request):
    if request.method == "POST":
        email = request.POST.get('email')
        msg = request.POST.get('message')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, "Please enter a valid email address.")
            return redirect('help')
        try:
            send_message_to_pintu.delay(email,msg)
            messages.success(request, "message sent successfully!")
        except Exception as e:
            messages.error(request, f"Something went wrong!{e}")
        print(f"email:", email)
        print(f"message:", msg)
        messages.success(request, "Your message has been sent!")
        return redirect('help')
    else:
        return redirect('help')


def search_result(request):
    query = request.GET.get('query', '')  # Get the search input
    results = []

    if query:
        # Search in product name and description (case-insensitive)
        results = Product.objects.filter(
            title__icontains=query
        ) | Product.objects.filter(
            category__icontains=query
        )

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'user_info/search_result.html', context)


@csrf_exempt
def payments_view(request, product_id):
    address = UserAddress.objects.filter(user=request.user).last()
    product = get_object_or_404(Product, id=product_id)
    print("id payment", settings.RAZORPAY_KEY_ID)
    print("hello work")

    order_data = {
        'amount': int(product.price * 100),   # Razorpay takes paisa
        'currency': "INR",
        'payment_capture': '1'
    }

# abbi order create karna hai

    razorpay_order = client.order.create(data=order_data)

    # Save order in DB (pending status initially)
    Order.objects.create(
        user=request.user,
        product=product,
        amount=product.price,
        razorpay_order_id=razorpay_order['id'],
        status="PENDING"  # keep status until payment success
    )

    context = {
        "product": product,
        "address": address,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": order_data['amount'],
        "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
        "currency": order_data['currency'],
        "razorpay_order_id": razorpay_order['id'],
        "user": request.user,
    }

    return render(request, "user_info/payment.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            params_dict = {
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            }

            # Verify signature
            client.utility.verify_payment_signature(params_dict)

            # Update order in DB
            order = Order.objects.get(
                razorpay_order_id=data["razorpay_order_id"])
            order.razorpay_payment_id = data["razorpay_payment_id"]
            order.razorpay_signature = data["razorpay_signature"]
            order.status = "SUCCESS"
            order.save()

            return JsonResponse({"status": "Payment Successful"})

        except Exception as e:
            print("Payment verification failed:", e)
            return HttpResponseBadRequest("Payment Verification Failed")


@csrf_exempt
def payments_cart_view(request):
    # get latest address
    user_info = userInfo.objects.get(user=request.user)
    address = UserAddress.objects.filter(user=request.user).last()
    total_amount = 0

    # get the user's cart
    cart = Cart.objects.filter(user=user_info).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart")

    cart_items = cart.items.all()

    # calculate total amount
    total_amount = sum(item.get_total_price() for item in cart_items)

    order_data = {
        "amount": int(total_amount * 100),  # Razorpay needs paisa
        "currency": "INR",
        "payment_capture": "1",
    }

    # create Razorpay order
    razorpay_order = client.order.create(data=order_data)

    # create local Order
    order = Order.objects.create(
        user=request.user,
        amount=total_amount,
        razorpay_order_id=razorpay_order["id"],
        status="PENDING"
    )

    # create OrderItems from CartItems
    for item in cart_items:
        OrderItems.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    # clear cart after order
    # cart.items.all().delete()

    context = {
        "order": order,
        "address": address,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": order_data["amount"],
        "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
        "currency": order_data["currency"],
        "razorpay_order_id": razorpay_order["id"],
        "user": request.user,
    }

    return render(request, "user_info/payment.html", context)

def pay_on_delivery(request,product_id):
    address = UserAddress.objects.filter(user=request.user).last()
    product = get_object_or_404(Product, id=product_id)
    get_user=request.user
    user_contact = get_object_or_404(SellerProfile,user = request.user)
    order_items = Order.objects.filter(status = 'SUCCESS')
    
    print("Cash on delivery.")
    if not address:
        messages.error(request,"Please Enter a Valid Address Before placing your order")
        return redirect('address')
    try:
        with transaction.atomic():
            order = Order.objects.filter(
                user=request.user,
                product=product,
                status="PENDING"
            ).last()
            if order:
                order.status = "SUCCESS"
                order.save()
                messages.success(request,"your order has been placed successfully with Cash on Delivery")
                order_confirmation.delay(get_user.username,get_user.email,product.title,address.city,address.pincode)
                
            else :
                messages.error(request,"Something went wrong")
                return redirect('cart_view')          
    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect("cart")  # or any relevant page
    
    context = {
        'address':address,
        "product":product,
        'order':order,
        'get_user':get_user,
        'user':user_contact,
        'order_items':order_items   
    }
    return render(request,"user_info/order_placed.html")
    

def order_placed_view(request):
    if request.user.is_authenticated:
        address = UserAddress.objects.filter(user=request.user).last()
        get_user=request.user
        user_contact = get_object_or_404(SellerProfile,user = request.user)
        order_items = Order.objects.filter(status = 'SUCCESS',user = get_user)
        context = {
            'address':address,
            'get_user':get_user,
            'user':user_contact,
            'order_items':order_items
        }
        return render(request,"user_info/order_placed.html",context)

    return render(request,"user_info/login.html")

    # return redirect('payments')
@login_required

def cancel_item(request,order_id):
    order = get_object_or_404(Order,user = request.user ,razorpay_order_id = order_id)
    order.status = "FAILED"
    order.save()
    messages.success(request, "Your order has been cancelled.")
    return redirect('order-placed')
    
        
    
    
def terms_and_condition(request):
    return render(request,"user_info/terms.html")
    
    