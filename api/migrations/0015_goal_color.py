# Generated by Django 5.0 on 2024-01-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_todo_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='color',
            field=models.CharField(default='white', max_length=25),
        ),
    ]
