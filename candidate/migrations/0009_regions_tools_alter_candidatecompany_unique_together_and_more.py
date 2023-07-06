# Generated by Django 4.1.5 on 2023-06-23 10:27

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_custompermission_options'),
        ('candidate', '0008_selectedcandidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('region', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='candidatecompany',
            unique_together={('company', 'candidate')},
        ),
        migrations.AlterUniqueTogether(
            name='selectedcandidate',
            unique_together={('company', 'candidate')},
        ),
        migrations.CreateModel(
            name='CandidateTools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate')),
                ('tool', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.tools')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateRegions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.regions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(default='N/A', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, null=True, size=None)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate')),
            ],
            options={
                'unique_together': {('name', 'candidate')},
            },
        ),
    ]
