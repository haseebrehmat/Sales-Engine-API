# Generated by Django 4.1.5 on 2023-04-17 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0006_jobdetail_is_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedjobstatus',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appliedjobstatus',
            name='resume',
            field=models.TextField(blank=True, null=True),
        ),
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
        migrations.AlterField(
            model_name='blacklistjobs',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blacklistjobs',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
