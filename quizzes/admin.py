from django.contrib import admin
from .models import User, Quiz, Question, Game, Player, MarkedQuestion

# Register your models here.
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(MarkedQuestion)
