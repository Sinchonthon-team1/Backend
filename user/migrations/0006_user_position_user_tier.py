# Generated by Django 5.0.7 on 2024-08-23 21:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_user_puuid_user_tag_line"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="position",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="user",
            name="tier",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
