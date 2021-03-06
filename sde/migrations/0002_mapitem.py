# Generated by Django 2.1.7 on 2019-03-24 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, null=True)),
                ('x', models.FloatField(default=0)),
                ('y', models.FloatField(default=0)),
                ('z', models.FloatField(default=0)),
                ('system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='map_items', to='sde.System')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_items', to='sde.Type')),
            ],
        ),
    ]
