# Generated by Django 4.1.5 on 2023-04-28 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0012_remove_jobdetail_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
