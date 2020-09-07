# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-07 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equip',
            old_name='is_apply_a',
            new_name='is_on',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='history',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='is_apply_b',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='equip',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='equip',
            name='description',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='equip',
            name='location',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='equip',
            name='phone_number',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='equip',
            name='provider_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equip',
            name='reason',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='equip',
            name='rent_exp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equip',
            name='rent_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equip',
            name='rent_user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equip',
            name='rent_user_name',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='equip',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equip',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='equip',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='equip',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
