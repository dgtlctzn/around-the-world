# Generated by Django 3.1.3 on 2020-11-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destinations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=200)),
                ('been', models.BooleanField(default=False)),
                ('want_to_go', models.BooleanField(default=False)),
            ],
        ),
    ]