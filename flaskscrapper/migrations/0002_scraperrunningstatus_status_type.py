# Generated by Django 4.1.5 on 2024-03-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flaskscrapper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraperrunningstatus',
            name='status_type',
            field=models.CharField(choices=[('start_stop', 'Start Stop'), ('running', 'Running')], default='running', max_length=200),
        ),
    ]
