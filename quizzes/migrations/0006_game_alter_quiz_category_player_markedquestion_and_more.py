# Generated by Django 4.2.5 on 2024-01-18 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_alter_quiz_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('time', models.BooleanField()),
                ('time_per_question', models.IntegerField()),
                ('time_total', models.IntegerField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.CharField(choices=[('No Category', 'No category'), ('Fashion', 'Fashion'), ('History', 'History'), ('School', 'School')], default='No Category Listed', max_length=18),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('question', models.IntegerField()),
                ('question_time', models.DateTimeField(auto_now_add=True)),
                ('total_time', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='quizzes.game')),
            ],
        ),
        migrations.CreateModel(
            name='MarkedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=128)),
                ('result', models.BooleanField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='quizzes.player')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz'),
        ),
    ]
