# Generated by Django 3.1.3 on 2021-01-11 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledgbook', '0016_auto_20210111_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcathecd',
            name='use_yn',
            field=models.CharField(blank=True, default='Y', max_length=2, null=True),
        ),
    ]
