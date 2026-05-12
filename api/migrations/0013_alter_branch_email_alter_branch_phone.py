# Generated manually to fix schema mismatch: phone was varchar(20), email was NOT NULL

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_headpastor_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='phone',
            field=models.TextField(help_text='Phone number(s) separated by commas (e.g., +233 20 123 4567, +233 30 987 6543)'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
