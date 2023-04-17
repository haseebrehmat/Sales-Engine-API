# Generated by Django 4.1.5 on 2023-04-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_scraper', '0010_alter_schedulersync_job_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allsyncconfig',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='allsyncconfig',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobsourcequery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobsourcequery',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedulersettings',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedulersettings',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedulersync',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedulersync',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='scraperlogs',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='scraperlogs',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
