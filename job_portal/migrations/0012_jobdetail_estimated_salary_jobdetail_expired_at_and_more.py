from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0011_blockjobcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetail',
            name='estimated_salary',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='expired_at',
            field=models.DateTimeField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='job_role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='salary_format',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='salary_max',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='salary_min',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
