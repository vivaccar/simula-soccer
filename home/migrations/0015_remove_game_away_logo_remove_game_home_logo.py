# Generated by Django 5.0.4 on 2024-05-14 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_team_aproveitamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='away_logo',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_logo',
        ),
    ]
