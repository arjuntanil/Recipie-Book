# Generated by Django 5.0.2 on 2025-04-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
