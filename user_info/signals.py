# user_info/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import SellerProfile

@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    print("its working..............")
    if created:
        base_slug = slugify(instance.username)
        slug = base_slug
        counter = 1
        while SellerProfile.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        SellerProfile.objects.create(user=instance, slug=slug)
        print(f"✅ SellerProfile created for {instance.username} with slug {slug}")
        

    
