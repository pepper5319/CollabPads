# Generated by Django 2.1.1 on 2018-09-21 20:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180921_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listobject',
            name='collaborators',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
