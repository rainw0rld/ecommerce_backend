# Generated by Django 3.2.3 on 2021-06-16 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0003_auto_20210616_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productalbum',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album', to='storefront.productdetail'),
        ),
    ]
