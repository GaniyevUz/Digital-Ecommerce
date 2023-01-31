# Generated by Django 4.1.5 on 2023-01-31 10:23

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Shop Category',
                'verbose_name_plural': 'Shop Categories',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Shop Currency',
                'verbose_name_plural': 'Shop Currencies',
            },
        ),
        migrations.CreateModel(
            name='PaymentProviders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='payment_providers/')),
                ('type', models.CharField(max_length=255)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('fields', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('languages', multiselectfield.db.fields.MultiSelectField(choices=[('uz', "O'zbek"), ('ru', 'РУССКИЙ'), ('en', 'ENGLISH')], max_length=15)),
                ('delivery_types', multiselectfield.db.fields.MultiSelectField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], max_length=15)),
                ('about_us', models.CharField(blank=True, max_length=1024, null=True)),
                ('delivery_price', models.IntegerField(blank=True, null=True, verbose_name='Delivery Price')),
                ('delivery_price_per_km', models.IntegerField(blank=True, null=True, verbose_name='Delivery Price Per KM')),
                ('minimum_delivery_price', models.IntegerField(blank=True, null=True)),
                ('free_delivery', models.BooleanField(blank=True, null=True)),
                ('about_us_image', models.ImageField(blank=True, null=True, upload_to='shops/')),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('has_terminal', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('starts_at', models.DateTimeField(blank=True, null=True)),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('delivery_terms', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('shop_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.category')),
                ('shop_currency', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.currency')),
            ],
        ),
    ]
