# Generated by Django 4.1.5 on 2023-01-31 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0002_prijava_odluka_donešena'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prijava',
            name='dokument',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
