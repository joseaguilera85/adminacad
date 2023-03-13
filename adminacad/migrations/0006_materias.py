# Generated by Django 4.1.7 on 2023-03-11 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("adminacad", "0005_alter_student_identificacion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Materias",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("clave_materia", models.CharField(max_length=100)),
                (
                    "grado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="adminacad.salones",
                    ),
                ),
            ],
        ),
    ]
