# Generated by Django 3.0.4 on 2020-09-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200905_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]
