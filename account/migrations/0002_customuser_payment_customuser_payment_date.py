# Generated by Django 4.2.6 on 2023-12-03 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]