# Generated by Django 2.0.3 on 2018-04-09 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ilmoitukset', '0002_ilmoitus_points'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Haaste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('time', models.CharField(max_length=500)),
                ('place', models.CharField(max_length=500)),
                ('ilmoitus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='haaste', to='ilmoitukset.Ilmoitus')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='haaste', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]