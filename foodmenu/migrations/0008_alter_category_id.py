# Generated by Django 5.0 on 2023-12-21 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmenu', '0007_category_created_at_category_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]