# Generated by Django 3.1.2 on 2021-03-23 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=150)),
                ('destination', models.CharField(max_length=150)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
