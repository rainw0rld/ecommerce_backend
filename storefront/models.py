from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField()
    thumbnail = models.ImageField(upload_to='media/img/title_img/', null=True)

    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, default='UNKNOWN')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    description = models.TextField(null=True)
    viewcount = models.IntegerField(default=0)

    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE, null=True)


class ProductAlbum(models.Model):
    product = models.ForeignKey(ProductDetail, related_name='album', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/img/album_img', null=True)