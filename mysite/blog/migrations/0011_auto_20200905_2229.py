# Generated by Django 3.0.4 on 2020-09-06 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200905_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='cooking_method',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='cooking_method',
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.CharField(default='dale', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='quantity',
            field=models.CharField(default=1, max_length=20),
        ),
    ]
