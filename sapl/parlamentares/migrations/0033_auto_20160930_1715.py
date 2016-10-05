# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-30 20:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0032_frenteproxymasterdetail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FrenteProxyMasterDetail',
        ),
        migrations.CreateModel(
            name='FrenteParlamentar',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'Frente',
                'verbose_name_plural': 'Frentes',
            },
            bases=('parlamentares.frente',),
        ),
    ]