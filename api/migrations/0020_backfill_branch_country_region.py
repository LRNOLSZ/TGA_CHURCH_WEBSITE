from django.db import migrations

CITY_TO_REGION = {
    "Accra": "Greater Accra",
    "Kumasi": "Ashanti",
    "Takoradi": "Western",
}


def backfill(apps, schema_editor):
    Branch = apps.get_model('api', 'Branch')
    Country = apps.get_model('api', 'Country')
    Region = apps.get_model('api', 'Region')

    ghana, _ = Country.objects.get_or_create(name="Ghana", defaults={"continent": "AF"})

    for branch in Branch.objects.filter(country__isnull=True):
        branch.country = ghana
        for city, region_name in CITY_TO_REGION.items():
            if city.lower() in (branch.name or "").lower() or city.lower() in (branch.location or "").lower():
                branch.region = Region.objects.filter(country=ghana, name=region_name).first()
                break
        branch.save(update_fields=["country", "region"])


def unbackfill(apps, schema_editor):
    Branch = apps.get_model('api', 'Branch')
    Branch.objects.update(country=None, region=None)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_branch_country_region'),
    ]

    operations = [
        migrations.RunPython(backfill, unbackfill),
    ]
