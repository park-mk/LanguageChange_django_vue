# Generated by Django 3.1.1 on 2020-09-13 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='reason_pro',
            field=models.CharField(default='', max_length=3000),
        ),
    ]