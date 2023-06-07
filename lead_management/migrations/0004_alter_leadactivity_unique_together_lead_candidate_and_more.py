from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0007_candidatecompany'),
        ('lead_management', '0003_companystatus_created_at_companystatus_updated_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leadactivity',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='lead',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate'),
        ),
        migrations.AddField(
            model_name='leadactivity',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate'),
        ),
        migrations.AlterUniqueTogether(
            name='leadactivity',
            unique_together={('lead', 'company_status', 'phase', 'candidate')},
        ),
    ]
