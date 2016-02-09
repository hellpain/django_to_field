# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(to_field='slug', to='example.ProductCollection'),
        ),
    ]
