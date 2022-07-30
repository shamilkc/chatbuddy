# Generated by Django 4.0.6 on 2022-07-29 13:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_alter_room_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='participents',
            field=models.ManyToManyField(blank=True, related_name='participents', to=settings.AUTH_USER_MODEL),
        ),
    ]