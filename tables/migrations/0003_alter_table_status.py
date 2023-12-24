# Generated by Django 5.0 on 2023-12-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_reservation_created_at_reservation_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='status',
            field=models.CharField(choices=[('R', 'Reserved'), ('E', 'Empty'), ('F', 'Full'), ('T', 'TakeAway')], default='E', max_length=1),
        ),
    ]