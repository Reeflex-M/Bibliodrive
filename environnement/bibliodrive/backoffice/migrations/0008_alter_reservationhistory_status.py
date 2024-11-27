# Generated by Django 5.1.2 on 2024-11-27 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0007_alter_reservationhistory_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationhistory',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('CANCELLED', 'Annulée'), ('ADMIN_CANCELLED', 'Annulée par admin')], max_length=20),
        ),
    ]
