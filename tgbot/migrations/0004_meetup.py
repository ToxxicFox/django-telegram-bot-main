# Generated by Django 3.2.10 on 2021-12-25 11:07

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('amountListeners', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('users', models.ManyToManyField(to='tgbot.User')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            managers=[
                ('admins', django.db.models.manager.Manager()),
            ],
        ),
    ]
