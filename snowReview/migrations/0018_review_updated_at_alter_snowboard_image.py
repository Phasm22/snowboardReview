# Generated by Django 5.0.3 on 2024-04-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snowReview', '0017_alter_snowboard_brand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='snowboard',
            name='image',
            field=models.ImageField(default='snowboards/blank.jpg', null=True, upload_to='snowboards/'),
        ),
    ]