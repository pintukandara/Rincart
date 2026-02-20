from .models import userInfo
from celery import shared_task
from django.core.mail import send_mail
import random


@shared_task
def send_verification_code(email,otp):
          
    send_mail(
                'Your OTP Code',
                f'Thank You For Registration \n Your OTP for Verification is: {otp}',
                'pintukandara124@gmail.com',
                [email],
                fail_silently=False
            )
    
@shared_task
def password_reset_request(email,username,reset_url):
    send_mail(
                'Password Reset Request',
                f'Hi {username},\n\nPlease click the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email.',
                'pintukandara124@gmail.com',
                [email],
                fail_silently=False

    )
@shared_task
def send_message_to_pintu(email,msg):
    send_mail(
                subject=f"New message from {email}",
                message=msg,
                from_email=email,
                recipient_list=["pintukandara124@gmail.com"],
                fail_silently=False
            )
@shared_task
def order_confirmation(username,email,product_title,address_city,address_pincode):
                    send_mail(
            'Order Confirmation',
            f'Congratulations {username},\n\n'
            f'Your order has been placed for {product_title} and will be delivered to '
            f'{address_city}, {address_pincode} within 6-7 days.\n',
            'pintukandara124@gmail.com',
            [email],
            fail_silently=False   
        )