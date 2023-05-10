# Generated by Django 4.1.5 on 2023-05-05 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pseudos', '0002_alter_skills_options_verticals_identity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('vertical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pseudos.verticals')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
