# Generated by Django 4.1.5 on 2023-04-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pseudos', '0012_alter_education_end_date_alter_education_start_date'),
        ('authentication', '0014_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='pseudos',
            field=models.ManyToManyField(related_name='pseudos', to='pseudos.pseudos'),
        ),
    ]
