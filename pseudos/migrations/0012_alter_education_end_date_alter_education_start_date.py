# Generated by Django 4.1.5 on 2023-04-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pseudos', '0011_alter_experience_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
