# Generated by Django 3.0.7 on 2020-08-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral1', '0002_referralrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralfirst',
            name='refertimes',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
