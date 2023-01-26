# Generated by Django 4.1.5 on 2023-01-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/%m')),
                ('price', models.IntegerField()),
                ('in_availability', models.BooleanField(default=True)),
                ('length', models.CharField(blank=True, max_length=50, null=True)),
                ('width', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('length_class', models.CharField(blank=True, choices=[('m', 'Metre'), ('cm', 'CM')], max_length=10, null=True)),
                ('weight_class', models.CharField(blank=True, choices=[('kg', 'KG'), ('gram', 'Gram')], max_length=10, null=True)),
            ],
        ),
    ]
