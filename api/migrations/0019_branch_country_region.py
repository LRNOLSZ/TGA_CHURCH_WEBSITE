from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_seed_ghana_country_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branches', to='api.country'),
        ),
        migrations.AddField(
            model_name='branch',
            name='region',
            field=models.ForeignKey(blank=True, help_text='Optional — only for countries that are subdivided into regions', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branches', to='api.region'),
        ),
    ]
