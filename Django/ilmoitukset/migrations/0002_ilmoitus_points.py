# Generated by Django 2.0.3 on 2018-03-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoitukset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ilmoitus',
            name='points',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
