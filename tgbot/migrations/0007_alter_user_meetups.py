# Generated by Django 3.2.10 on 2021-12-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0006_auto_20211225_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='meetups',
            field=models.ManyToManyField(blank=True, to='tgbot.MeetUp'),
        ),
    ]
