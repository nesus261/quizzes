# Generated by Django 4.2.5 on 2024-01-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0007_alter_player_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='running',
            field=models.BooleanField(default=False),
        ),
    ]
