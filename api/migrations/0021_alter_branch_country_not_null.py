from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_backfill_branch_country_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='branches', to='api.country'),
        ),
    ]
