from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0022_alter_edithistory_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobarchive',
            name='estimated_salary',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobarchive',
            name='salary_format',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobarchive',
            name='salary_max',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobarchive',
            name='salary_min',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
