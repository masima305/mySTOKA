# Generated by Django 3.1.3 on 2021-01-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledgbook', '0014_auto_20210110_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinfo',
            name='staple_item',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='stock_name',
            field=models.CharField(max_length=20),
        ),
    ]