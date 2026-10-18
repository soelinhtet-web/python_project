from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="main_category", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class FeatureModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(upload_to="feature_image", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name
    
class MainheroModel(models.Model):
    maintitle = models.TextField()
    descriptionTitle = models.TextField()
    maindescription = models.TextField()
    mainimage = models.ImageField(upload_to="main_image", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.maintitle
    
class AboutModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class BrandModel(models.Model):
    image = models.ImageField(upload_to='brand/', blank=True, null=True)

    def __str__(self):
        return self.image
    
class CardModel(models.Model):
    name = models.CharField(max_length=250)
    size = models.CharField(max_length=10)
    starrating = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='brand/', blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.TextField()

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class AddToCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(CardModel, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 NEW FIELD (notification system)
    is_seen = models.BooleanField(default=False)

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(CardModel, on_delete=models.CASCADE)

    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total(self):
        return self.price * self.quantity
    
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)



from django.db import models


class FooterSetting(models.Model):
    brand_name = models.CharField(
        max_length=150, default="StyleNest ✦"
    )
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    creator = models.CharField(
        max_length=150, default="OdayZone (Mg SLH)"
    )

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = "Footer Setting"
        verbose_name_plural = "Footer Settings"


class FooterLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
