# Generated by Django 4.1.5 on 2023-06-20 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0009_alter_jobdetail_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetail',
            name='job_applied',
            field=models.CharField(default='not applied', max_length=300),
        ),
    ]
