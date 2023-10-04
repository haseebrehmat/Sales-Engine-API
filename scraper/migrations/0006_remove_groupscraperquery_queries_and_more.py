from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20230811_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupscraperquery',
            name='queries',
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='job_source',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='job_type',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groupscraperquery',
            name='status',
            field=models.CharField(default='remaining', max_length=250),
        ),
        migrations.AlterField(
            model_name='groupscraperquery',
            name='group_scraper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraper.groupscraper'),
        ),
    ]
