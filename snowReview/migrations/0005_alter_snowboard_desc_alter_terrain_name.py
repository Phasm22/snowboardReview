# Generated by Django 5.0.3 on 2024-03-28 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snowReview', '0004_terrain_snowboard_terrain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snowboard',
            name='desc',
            field=models.CharField(default='No description available', max_length=500),
        ),
        migrations.AlterField(
            model_name='terrain',
            name='name',
            field=models.CharField(choices=[('Freestyle', 'Freestyle'), ('All-Mountain', 'All-Mountain'), ('Freeride', 'Freeride'), ('Powder', 'Powder')], max_length=50),
        ),
    ]
