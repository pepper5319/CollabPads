# Generated by Django 2.1.1 on 2018-09-26 19:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180922_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='liked_users',
        ),
        migrations.AddField(
            model_name='item',
            name='liked_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listobject',
            name='name',
            field=models.CharField(default='My List', max_length=255),
        ),
    ]