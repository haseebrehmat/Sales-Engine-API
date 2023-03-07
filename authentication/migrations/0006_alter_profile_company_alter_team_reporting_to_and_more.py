# Generated by Django 4.1.5 on 2023-03-07 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_delete_companyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.company'),
        ),
        migrations.AlterField(
            model_name='team',
            name='reporting_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(blank=True, help_text='The roles of this user belongs to. A user will get all permissions granted to each of their roles.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.role', verbose_name='roles'),
        ),
    ]
