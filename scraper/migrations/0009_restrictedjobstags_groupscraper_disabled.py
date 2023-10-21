# Generated by Django 4.1.5 on 2023-10-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_jobsource_groupscraper_running_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictedJobsTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('tag', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='groupscraper',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
