# Generated by Django 2.0.1 on 2018-01-11 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0002_auto_20180111_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
