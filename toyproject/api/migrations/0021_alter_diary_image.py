# Generated by Django 5.0 on 2024-01-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_diary_color_diary_emoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
