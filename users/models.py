from django.db import models
from django.utils import timezone
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from functools import reduce
from operator import add
import decimal

from django.contrib.auth.models import AbstractUser, BaseUserManager
from storefront.models import Product


class CustomerManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(email, first_name, last_name, password, **kwargs)

    def create_user(self, email, first_name, last_name, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class CartManager(models.Manager):
    QuerySet = models.QuerySet

    def get_query_set(self):
        return self.QuerySet(self.model, self._db)

    def get(self, user):
        return self.get_query_set().get(user=user, status='cart')

    def create(self, *args, **kwargs):
        return self.get_query_set().create(*args, **kwargs)

    def get_or_create(self, user, *args, **kwargs):
        if not self.get_query_set().filter(user=user, status='cart').exists():
            return self.create(user=user)
        return self.get(user)


class OrdersManager(models.Manager):
    QuerySet = models.QuerySet

    def get_query_set(self):
        return self.QuerySet(self.model, self._db)

    def get_queryset(self):
        return self.get_query_set().exclude(status='cart')


class Address(models.Model):
    street_1 = models.CharField(max_length=40)
    street_2 = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=7)
    region = models.CharField(max_length=25)
    country = models.CharField(max_length=25)

    user = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)


class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'cart'),
        ('received', 'received'),
        ('processing', 'processing'),
        ('in_delivery', 'in delivery'),
        ('delivered', 'delivered'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'cash'),
        ('CARD', 'card'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('success', 'successful')
    )

    user = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='cart')
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=8, choices=PAYMENT_STATUS_CHOICES, blank=True, null=True)
    tracking_number = models.CharField(max_length=20, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)

    objects = models.Manager()
    orders = OrdersManager()
    cart = CartManager()

    def set_price(self):
        item_prices = OrderItem.objects.filter(order=self.id).values_list('price', flat=True)
        price = reduce(add, item_prices, decimal.Decimal(0))
        self.total = price
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_to_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_to_order')
    qty = models.IntegerField(default=1)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)

    def update_price(self):
        price = self.product.price * self.qty
        self.price = price


@receiver(pre_save, sender=OrderItem)
def orderitem_pre_save(sender, instance, *args, **kwargs):
    if instance.qty > instance.product.stock:
        instance.qty = instance.product.stock
    instance.update_price()


@receiver(post_save, sender=Customer)
def customer_post_save(sender, instance, *args, **kwargs):
    send_mail(
        'Welcome to my website!',
        f'Hey, {instance.first_name}! Thanks for signing up, hope you enjoy our serivces!',
        None,
        [instance.email],
        fail_silently=True
    )


