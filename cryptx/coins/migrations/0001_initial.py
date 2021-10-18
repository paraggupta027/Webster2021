# Generated by Django 3.2.8 on 2021-10-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('symbol', models.CharField(default='', max_length=30)),
                ('real_time_url', models.URLField(verbose_name='REAL TIME URL')),
            ],
        ),
    ]