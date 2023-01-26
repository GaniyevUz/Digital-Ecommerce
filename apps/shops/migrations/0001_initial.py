# Generated by Django 4.1.5 on 2023-01-26 13:07

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='shop/categories/')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'category Translation',
                'db_table': 'shops_category_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Shop Currency',
                'verbose_name_plural': 'Shop Currencies',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
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
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('languages', multiselectfield.db.fields.MultiSelectField(choices=[('uz', "O'zbek"), ('ru', 'РУССКИЙ'), ('en', 'ENGLISH')], max_length=15)),
                ('about_us', models.CharField(blank=True, max_length=1024, null=True)),
                ('delivery_price', models.IntegerField(blank=True, null=True, verbose_name='Delivery Price')),
                ('delivery_price_per_km', models.IntegerField(blank=True, null=True, verbose_name='Delivery Price Per KM')),
                ('minimum_delivery_price', models.IntegerField(blank=True, null=True)),
                ('free_delivery', models.BooleanField(blank=True, null=True)),
                ('about_us_image', models.ImageField(blank=True, null=True, upload_to='shops/')),
                ('expired_at', models.DateTimeField(blank=True, null=True)),
                ('has_terminal', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('delivery_terms', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('related_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shopcategory')),
            ],
        ),
    ]
