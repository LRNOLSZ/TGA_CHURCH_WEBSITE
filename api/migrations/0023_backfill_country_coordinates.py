from django.db import migrations

from api.country_coordinates import COUNTRY_COORDINATES


def backfill_coordinates(apps, schema_editor):
    Country = apps.get_model('api', 'Country')
    for country in Country.objects.all():
        coords = COUNTRY_COORDINATES.get(country.name)
        if coords:
            country.latitude, country.longitude = coords
            country.save(update_fields=['latitude', 'longitude'])


def noop_reverse(apps, schema_editor):
    Country = apps.get_model('api', 'Country')
    Country.objects.update(latitude=None, longitude=None)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_country_latitude_longitude_choices'),
    ]

    operations = [
        migrations.RunPython(backfill_coordinates, noop_reverse),
    ]
