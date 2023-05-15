from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllSyncConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobSourceQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('job_source', models.CharField(max_length=100, unique=True)),
                ('queries', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchedulerSettings',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_based', models.BooleanField(default=False)),
                ('interval_based', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('interval', models.IntegerField(blank=True, default=0, null=True)),
                ('interval_type', models.CharField(blank=True, max_length=100, null=True)),
                ('job_source', models.CharField(default='', max_length=100)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ScraperLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('job_source', models.CharField(default='', max_length=250)),
                ('total_jobs', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchedulerSync',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('job_source', models.CharField(blank=True, max_length=200, null=True)),
                ('running', models.BooleanField(default=False)),
                ('type', models.CharField(default='instant', max_length=250)),
            ],
            options={
                'unique_together': {('job_source', 'type')},
            },
        ),
    ]
