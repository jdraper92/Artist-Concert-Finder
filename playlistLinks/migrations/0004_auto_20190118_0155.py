# Generated by Django 2.1.5 on 2019-01-18 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlistLinks', '0003_concert_last_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last', models.DateTimeField(verbose_name='last updated')),
            ],
        ),
        migrations.RemoveField(
            model_name='concert',
            name='last_updated',
        ),
    ]
