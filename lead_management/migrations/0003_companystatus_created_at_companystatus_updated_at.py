# Generated by Django 4.1.5 on 2023-06-01 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead_management', '0002_remove_lead_user_alter_lead_applied_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='companystatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='companystatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
