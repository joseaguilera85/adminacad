# Generated by Django 4.1.5 on 2024-11-13 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("egresos", "0005_remove_egreso_amount_remove_egreso_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorderitem",
            name="purchase_order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="egresos.purchaseorder",
            ),
        ),
    ]
