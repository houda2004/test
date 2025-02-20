# Generated by Django 5.1.5 on 2025-01-28 11:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personnale', '0003_emailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverification',
            name='expires_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='code',
            field=models.CharField(max_length=10),
        ),
    ]
