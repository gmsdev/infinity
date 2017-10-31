# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-31 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoKeypair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name=[(0, 'IPDB')])),
                ('private_key', models.TextField(blank=True, null=True)),
                ('public_key', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
