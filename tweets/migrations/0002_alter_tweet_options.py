# Generated by Django 4.2.8 on 2024-02-11 11:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tweet",
            options={"ordering": ["-created_at"], "verbose_name": "ツイート", "verbose_name_plural": "ツイート"},
        ),
    ]
