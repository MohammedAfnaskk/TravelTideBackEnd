# Generated by Django 4.2.6 on 2023-12-05 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel_manager', '0006_alter_invitation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.BooleanField(default=False)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel_manager.mainplace')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]