# Generated by Django 5.0.3 on 2024-03-29 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snowReview', '0009_alter_size_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
