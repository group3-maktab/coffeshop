# Generated by Django 5.0 on 2023-12-19 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmenu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='picture_url',
        ),
        migrations.AddField(
            model_name='food',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='foodmenu.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='off',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
