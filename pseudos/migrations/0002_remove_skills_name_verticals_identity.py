# Generated by Django 4.1.5 on 2023-05-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pseudos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skills',
            name='name',
        ),
        migrations.AddField(
            model_name='verticals',
            name='identity',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
