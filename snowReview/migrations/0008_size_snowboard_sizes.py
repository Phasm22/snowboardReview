# Generated by Django 5.0.3 on 2024-03-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snowReview', '0007_alter_snowboard_flex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=4)),
            ],
        ),
        migrations.AddField(
            model_name='snowboard',
            name='sizes',
            field=models.ManyToManyField(to='snowReview.size'),
        ),
    ]