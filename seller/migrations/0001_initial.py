# Generated by Django 3.0.7 on 2020-07-19 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopname', models.CharField(max_length=50, null=True)),
                ('shopaddress', models.CharField(max_length=200, null=True)),
                ('shoplongitude', models.FloatField(default=0, null=True)),
                ('shoplatitude', models.FloatField(default=0, null=True)),
                ('shoppincodes', models.CharField(default=[], max_length=200)),
                ('shopphoto', models.ImageField(default='default/shopphotor.jpg', upload_to='shop/photo')),
                ('shopbanner', models.ImageField(default='default/shopbanner.jpg', upload_to='shop/banner')),
                ('status', models.BooleanField(default=True)),
                ('shopcategoty', models.CharField(choices=[('fashion', 'Fashion'), ('food', 'Food'), ('grocery', 'Grocery'), ('electronics', 'Electronics'), ('handcrafts', 'Handcrafts')], max_length=30, null=True)),
                ('review', models.FloatField(default=5.0)),
                ('homedelivery', models.BooleanField(default=0)),
                ('deliverycharge', models.FloatField(default=0)),
                ('freedelivery', models.BooleanField(default=0)),
                ('minpriceforfreedelivery', models.FloatField(default=499)),
                ('allindia', models.BooleanField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]