# Generated by Django 5.0 on 2024-01-29 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_todo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='mood',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
