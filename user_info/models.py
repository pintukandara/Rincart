# models.py
from django.contrib.auth.models import User
from django.db import models
import random
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError


import re

from django.core.validators import RegexValidator



class userInfo(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False,)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.user.username if self.user else "No user linked"


class Product(models.Model):
    categories = [
        ("Electronics", "Electronics"),
        ("Books", "Books"),
        ("Vehicle", "Vehicle"),
        ("Houses & Flat for Rent", "Houses & Flat for Rent"),
        ("Houses & Flat for Sell", "Houses & Flat for Sell"),
        ("furniture", "Furniture"),

    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=categories)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    slug = models.SlugField(max_length=50,
                            blank=False,
                            null=False,
                            db_index=True,
                            help_text="unique URL path for the post")
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null = True)

    def __str__(self):
        return f"{self.title} Posted by:{self.posted_by}"

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)


class UserAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('manual', 'Enter Manually'),
        ('live', 'Use Live Location')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=10, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True,)

    def __str__(self):
        return f"{self.user}, {self.city}"


class Cart(models.Model):
    user = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username}"


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, related_name="items",
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} {self.quantity} "
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
def validate_aadhaar(value):
    """ Aadhaar must be exactly 12 digits """
    if not re.fullmatch(r"\d{12}", value):
        raise ValidationError("Aadhaar number must be exactly 12 digits")

def validate_ifsc(value):
    """ IFSC: 4 letters + 0 + 6 digits """
    if not re.fullmatch(r"^[A-Z]{4}0\d{6}$", value):
        raise ValidationError("Invalid IFSC code format")

def validate_phone(value):
    """ Phone: 10 digits only (India standard) """
    if not re.fullmatch(r"\d{10}", value):
        raise ValidationError("Phone number must be 10 digits")





class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")

    mobile = models.CharField(
        max_length=15,
        unique=False,
        validators=[validate_phone],
        help_text="Enter a valid 10-digit phone number"
    )
    address = models.CharField(max_length=255)
    seller_email = models.ForeignKey(User, related_name="seller_email", on_delete=models.CASCADE,null=True,blank=True)

    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="Tell buyers about yourself.")

    joined_on = models.DateField(default=timezone.now)

    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11, validators=[validate_ifsc])
    adhaar_number = models.CharField(max_length=12, validators=[validate_aadhaar])

    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique URL for the seller"
    )

    def __str__(self):
        return f"{self.user.username}'s Seller Profile {self.slug}"

    def get_absolute_url(self):
        return reverse("seller_profile", args=[self.slug])

    def save(self, *args, **kwargs):
        # Auto-generate slug from username if not provided
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            while SellerProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=255, unique=True,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("SUCCESS", "Success"), ("FAILED", "Failed")],
        default="PENDING",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default= 1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.quantity*self.price