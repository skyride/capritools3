# Generated by Django 2.2.12 on 2020-06-13 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0003_faction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='anchored',
            field=models.BooleanField(null=True),
        ),
    ]
