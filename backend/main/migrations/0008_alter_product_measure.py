# Generated by Django 4.1.4 on 2022-12-29 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_historyproduct_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='measure',
            field=models.CharField(choices=[('Metrida', 'metr'), ('kg', 'kg'), ('sonida', 'number')], max_length=256),
        ),
    ]
