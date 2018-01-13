# Generated by Django 2.0.1 on 2018-01-12 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0009_auto_20180112_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='shop',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='DonStockServer.Shop', verbose_name='Магазин'),
        ),
    ]
