from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORIES = [
    ("No Category", "No category"),
    ("Fashion", "Fashion"),
    ("History", "History"),
    ("School", "School")
]


class User(AbstractUser):
    avatar = models.ImageField(upload_to='profile_pictures', null=True, blank=True)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    watching = models.ManyToManyField(User, blank=True, related_name="watched")
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)
    category = models.CharField(
        max_length=18,
        choices=CATEGORIES,
        default="No Category Listed",
    )

    def __str__(self):
        return f'{self.title}: {self.owner.username}'
    


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    query = models.CharField(max_length=256)
    image = models.ImageField(upload_to='questions_images', null=True, blank=True)
    answer = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.quiz.title}: {self.query}'


class Game(models.Model):
    code = models.CharField(max_length=6)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True) # models.SET_NULL,
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games", blank=True, null=True)
    running = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    show_player_answers = models.BooleanField(default=True)
    show_correct_answers = models.BooleanField(default=True)
    time = models.BooleanField()
    time_per_question = models.IntegerField()
    time_total = models.IntegerField()

    def __str__(self):
        return f'{self.code}'


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=32)
    question_time = models.DateTimeField(auto_now_add=True)
    total_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} in {self.game.quiz.title}'


class MarkedQuestion(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="marked")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="marked", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=128)
    result = models.BooleanField()

    def __str__(self):
        return f'{self.result} of {self.player.name}'
