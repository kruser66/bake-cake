# Generated by Django 4.2.3 on 2023-07-23 21:36

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_cakeuser_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(
                default="Адрес доставки", max_length=255, verbose_name="Адрес доставки"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="customer_email",
            field=models.EmailField(
                blank=True, max_length=100, null=True, verbose_name="email получателя"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="customer_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Имя получателя"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="customer_phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default="+79139791676",
                max_length=20,
                region=None,
                verbose_name="Телефон получателя",
            ),
            preserve_default=False,
        ),
    ]
