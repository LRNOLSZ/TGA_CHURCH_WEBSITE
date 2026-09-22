from django.db import migrations


GHANA_REGIONS = ["Greater Accra", "Ashanti", "Western"]


def seed_ghana(apps, schema_editor):
    Country = apps.get_model('api', 'Country')
    Region = apps.get_model('api', 'Region')
    ghana, _ = Country.objects.get_or_create(name="Ghana", defaults={"continent": "AF"})
    for region_name in GHANA_REGIONS:
        Region.objects.get_or_create(country=ghana, name=region_name)


def unseed_ghana(apps, schema_editor):
    Country = apps.get_model('api', 'Country')
    Country.objects.filter(name="Ghana").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_country_region'),
    ]

    operations = [
        migrations.RunPython(seed_ghana, unseed_ghana),
    ]
