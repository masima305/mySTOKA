# Generated by Django 3.1.3 on 2021-03-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledgbook', '0019_auto_20210111_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcathe',
            name='cathe_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stockcathecd',
            name='cathe_num',
            field=models.IntegerField(default=0),
        ),
    ]
