# Generated by Django 5.0 on 2023-12-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmenu', '0008_alter_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='foodimage',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]