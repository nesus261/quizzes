# Generated by Django 4.2.5 on 2024-01-26 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0008_game_running'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='question',
        ),
        migrations.AlterField(
            model_name='markedquestion',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marked', to='quizzes.player'),
        ),
    ]
