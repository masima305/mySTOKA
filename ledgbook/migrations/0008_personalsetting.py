# Generated by Django 3.1.3 on 2020-12-08 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledgbook', '0007_auto_20201204_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='personalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settingAddDeposit', models.CharField(max_length=1000)),
                ('settingChangeRate', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
