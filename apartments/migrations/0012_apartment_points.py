# Generated by Django 4.1.5 on 2024-12-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0011_project_tipo"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="points",
            field=models.JSONField(default=[[0, 0], [10, 10]]),
            preserve_default=False,
        ),
    ]
