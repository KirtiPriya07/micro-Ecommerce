# Generated by Django 4.1.13 on 2024-03-20 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_productattachment"),
    ]

    operations = [
        migrations.AddField(
            model_name="productattachment",
            name="name",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
