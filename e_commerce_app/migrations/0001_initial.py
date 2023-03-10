# Generated by Django 4.1.7 on 2023-03-07 09:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('familyName', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(default='+21622000000', max_length=20)),
                ('typeClient', models.CharField(choices=[('LOYAL', 'Loyal Customer'), ('NORMAL', 'Normal Customer'), ('VIP', 'Very Import Customer')], default='NORMAL', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='', max_length=100)),
                ('price', models.FloatField(default=0)),
                ('stock', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/product_images')),
                ('description', models.TextField(blank=True, null=True)),
                ('expirationDate', models.DateField(default=datetime.date(2023, 12, 31))),
                ('fabricationDate', models.DateField(default=datetime.date(2023, 3, 7))),
            ],
        ),
    ]
