# Generated by Django 4.1.1 on 2022-10-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movie_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='length',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]