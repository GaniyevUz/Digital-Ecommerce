# Generated by Django 4.1.6 on 2023-02-02 15:04

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(blank=True, max_length=225, null=True)),
                ('phone', models.CharField(max_length=225)),
                ('note', models.TextField(blank=True, null=True)),
                ('delivery_price', models.IntegerField(default=0)),
                ('total_price', models.IntegerField()),
                ('promo_code', models.CharField(blank=True, max_length=225, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrderTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('delivery_type', models.CharField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], max_length=15, verbose_name='Delivery Type')),
                ('status', models.CharField(choices=[('in_process', 'In Process'), ('ready', 'Ready'), ('picked_ip', 'Picked Up'), ('rejected', 'Rejected'), ('delivered', 'Delivered'), ('expired', 'Expired')], default='in_process', max_length=50, verbose_name='Status')),
                ('payment_type', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card')], default='cash', help_text='Choices: cash or card', max_length=225, verbose_name='Payment Type')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='orders.order')),
            ],
            options={
                'verbose_name': 'order Translation',
                'db_table': 'orders_order_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
