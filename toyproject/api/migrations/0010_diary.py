# Generated by Django 5.0 on 2023-12-30 06:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_todo_goal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('visibility', models.CharField(choices=[('PB', 'Public'), ('PR', 'Private'), ('FL', 'Followers')], default='FL', max_length=2)),
                ('mood', models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
