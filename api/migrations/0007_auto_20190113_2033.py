# Generated by Django 2.1.1 on 2019-01-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_oneoff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='assigned_list',
            field=models.CharField(max_length=6),
        ),
    ]
