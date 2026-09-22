from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_merchandise_available_sizes_merchandise_has_sizes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('continent', models.CharField(choices=[
                    ('AF', 'Africa'), ('AS', 'Asia'), ('EU', 'Europe'),
                    ('NA', 'North America'), ('SA', 'South America'),
                    ('OC', 'Oceania'), ('AN', 'Antarctica'),
                ], db_index=True, max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['continent', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='regions', to='api.country')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('country', 'name')},
            },
        ),
    ]
