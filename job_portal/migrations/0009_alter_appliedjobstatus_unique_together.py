# Generated by Django 4.1.5 on 2023-05-05 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0008_appliedjobstatus_vertical'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appliedjobstatus',
            unique_together=set(),
        ),
    ]
