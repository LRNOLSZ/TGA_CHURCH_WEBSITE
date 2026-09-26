from django.db import migrations

from api.region_data import REGION_DATA


def backfill_regions(apps, schema_editor):
    Country = apps.get_model('api', 'Country')
    Region = apps.get_model('api', 'Region')
    for country in Country.objects.all():
        for region_name in REGION_DATA.get(country.name, []):
            Region.objects.get_or_create(country=country, name=region_name)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_backfill_country_coordinates'),
    ]

    operations = [
        migrations.RunPython(backfill_regions, noop_reverse),
    ]
