# Generated by Django 4.1.5 on 2023-05-30 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_custompermission_options'),
        ('candidate', '0004_alter_candidate_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exposedcandidate',
            options={'default_permissions': ()},
        ),
        migrations.AlterUniqueTogether(
            name='exposedcandidate',
            unique_together={('candidate', 'company')},
        ),
        migrations.AlterModelTable(
            name='exposedcandidate',
            table='exposed_candidates',
        ),
    ]
