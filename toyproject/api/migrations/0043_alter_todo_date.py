# Generated by Django 5.0 on 2024-01-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_alter_diary_emoji_alter_like_emoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date',
            field=models.DateField(blank=True, default=''),
        ),
    ]
