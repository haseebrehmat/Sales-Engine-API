# Generated by Django 3.2.20 on 2023-07-25 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0009_regions_tools_alter_candidatecompany_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tools',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
