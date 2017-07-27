# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-27 20:54
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('claimed_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('assumed_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parents', models.ManyToManyField(blank=True, related_name='parent_comments', to='core.Comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommentSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('claimed_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('assumed_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Comment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContributionCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name=[(0, 'DOER'), (1, 'INVESTOR')])),
                ('matched_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('comment_snapshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CommentSnapshot')),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyPriceSerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('endpoint', models.TextField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourPriceSerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('endpoint', models.TextField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourPriceSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('currency', models.PositiveSmallIntegerField(default=1, verbose_name=[(0, 'HUR'), (1, 'EUR'), (2, 'USD'), (3, 'CNY'), (4, 'RUB'), (5, 'JPY'), (6, 'INR')])),
                ('currency_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CurrencyPriceSerie')),
                ('hour_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.HourPriceSerie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(default=5, verbose_name=[(0, 'Need'), (1, 'Goal'), (2, 'Idea'), (3, 'Plan'), (4, 'Step'), (5, 'Task')])),
                ('title', models.TextField()),
                ('body', models.TextField(blank=True, null=True)),
                ('editors', models.ManyToManyField(blank=True, related_name='topic_editors', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parents', models.ManyToManyField(blank=True, related_name='parent_topics', to='core.Topic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('payment_amount', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('payment_currency', models.PositiveSmallIntegerField(default=1, verbose_name=[(0, 'HUR'), (1, 'EUR'), (2, 'USD'), (3, 'CNY'), (4, 'RUB'), (5, 'JPY'), (6, 'INR')])),
                ('hour_price_in_payment_currency', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('donated_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('matched_hours', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Comment')),
                ('hour_price_snapshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.HourPriceSnapshot')),
                ('payment_recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('payment_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('snapshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CommentSnapshot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contributioncertificate',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Transaction'),
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Topic'),
        ),
    ]
