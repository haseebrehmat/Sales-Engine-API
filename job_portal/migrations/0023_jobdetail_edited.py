# Generated by Django 4.1.5 on 2023-08-22 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0022_alter_edithistory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetail',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
