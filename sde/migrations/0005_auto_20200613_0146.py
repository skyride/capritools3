# Generated by Django 2.2.12 on 2020-06-13 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0004_auto_20200613_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='anchorable',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='anchored',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
