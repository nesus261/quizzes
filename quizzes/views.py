from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import User, Quiz, Question, Game

import random


QUIZZES_PER_PAGE = 10
MY_QUIZZES_PER_PAGE = 4


@login_required(login_url='login', redirect_field_name=None)
def init_game_view(request):
    if request.method == "POST":
        clear_initialized_games(request.user)
        code = generateCode()
        quiz = Quiz.objects.get(id=request.POST["quiz_id"])
        creator = request.user
        show_player_answers = "true" in request.POST.getlist('show-player-answers')
        show_correct_answers = "true" in request.POST.getlist('show-correct-answers')
        time = "true" in request.POST.getlist('time-limit')
        time_per_question = request.POST["max-time-per-question"]
        time_total = request.POST["max-time-total"]
        try:
          game = Game(code=code, 
                      quiz=quiz, 
                      creator=creator, 
                      time=time, 
                      show_player_answers=show_player_answers, 
                      show_correct_answers=show_correct_answers, 
                      time_per_question=time_per_question, 
                      time_total=time_total)
          game.save()
        except IntegrityError:
            return JsonResponse({
                "message": {
                    "title": "Error",
                    "body": "Some unexpected error"
                }
            }, status=201)
        return JsonResponse({ "ok": 1, "code": code }, status=201)
    else:
        return HttpResponseRedirect(reverse("index"))


def clear_initialized_games(user):
    for game in Game.objects.filter(creator=user, running=False, finished=False):
        game.delete()


def generateCode():
    code = random.randint(100000,999999)
    try:
        Game.objects.get(code=code)
        return generateCode()
    except:
        return str(code)


def game_view(request, code):
    if request.method == "POST":
        pass
    else:
        try:
            game = Game.objects.get(code=code)
            if request.user == game.creator:
                return render(request, "quizzes/game_admin.html", {
                    "game": game,
                })
            else:
                return render(request, "quizzes/game.html", {
                    "game": game, 
                })
        except:
            return HttpResponseRedirect(reverse("index"))


def check_quiz_view(request, code):
    if request.method == "POST":
        try:
            game = Game.objects.get(code=code)
            if game.running or game.finished:
                return JsonResponse({ 
                  "message":{
                    "title": "Error",
                    "body": "Quiz finished or currently running" 
                  }
                }, status=207)
            else:
                return JsonResponse({ "ok": 1 }, status=201)
        except:
            return JsonResponse({ 
              "message":{
                "title": "Error",
                "body": "Quiz does not exist" 
              }
            }, status=206)


def quiz_view(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, "quizzes/quiz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all(),
        "favourite": quiz.watching.filter(username=request.user.username).first()
    })


@login_required(login_url='login', redirect_field_name=None)
def delete_quiz_view(request, id):
    if quiz := Quiz.objects.get(id=id, owner=request.user):
        quiz.delete()
        return HttpResponseRedirect(reverse("my_quizzes"))
    return HttpResponseRedirect(reverse("index"))
    

@login_required(login_url='login', redirect_field_name=None)
def edit_quiz_view(request, id):
    try:
        return render(request, "quizzes/add_quiz.html", {
            "quiz": Quiz.objects.get(id=id, owner=request.user)
        })
    except:
        return HttpResponseRedirect(reverse("index"))
    

@login_required(login_url='login', redirect_field_name=None)
def add_quiz_view(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        if not request.POST.get('query-0'):
            return JsonResponse({
                "message": {
                    "title": "Error",
                    "body": "The quiz must have at least one question"
                }
            }, status=201)
        title = request.POST['title']
        category = request.POST['category']
        description = request.POST['description']
        if not title or not description:
            return JsonResponse({"error": "Content cannot be empty"}, status=400)
        try:
          if request.POST.get('id'):
            if quiz := Quiz.objects.get(id=request.POST.get('id'), owner=request.user):
                quiz.title = title
                quiz.category = category
                quiz.description = description
                quiz.questions.all().delete()
                quiz.save()
            else:
                return HttpResponseRedirect(reverse("index"))
          else:
            quiz = Quiz(owner=request.user, title=title, category=category, description=description)
            quiz.save()
        except IntegrityError as e:
            print(e)
            return JsonResponse({
                "message": {
                    "title": "Error",
                    "body": "Title already taken"
                }
            }, status=201)
        for i in range(int(request.POST['questions_count'])):
            query = request.POST[f'query-{i}']
            image = request.FILES.get(f'image-{i}')
            answer = request.POST[f'answer-{i}']
            if not query or not answer:
                return JsonResponse({"error": "Content cannot be empty"}, status=400)
            question = Question(quiz=quiz, query=query, image=image, answer=answer)
            question.save()

        return JsonResponse({ "ok": 1, "quiz": quiz.id }, status=201)
    else:
        return render(request, "quizzes/add_quiz.html")


def index_view(request):
    paginator = Paginator(Quiz.objects.all(), QUIZZES_PER_PAGE)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    return render(request, "quizzes/quizzes.html", {
        "title": "Find quizzes",
        "quizzes": paginator.get_page(page_number)
    })


def search_view(request):
    paginator = Paginator(Quiz.objects.filter(title__contains=request.GET['q']), QUIZZES_PER_PAGE)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    return render(request, "quizzes/quizzes.html", {
        "title": "Find quizzes",
        "quizzes": paginator.get_page(page_number)
    })


def category_view(request, category):
    paginator = Paginator(Quiz.objects.filter(category=category), QUIZZES_PER_PAGE)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    return render(request, "quizzes/quizzes.html", {
        "title": category,
        "quizzes": paginator.get_page(page_number)
    })


@login_required(login_url='login', redirect_field_name=None)
def my_quizzes_view(request):
    if request.method == "GET":
        running = Paginator(Game.objects.filter(creator=request.user, running=True, finished=False), MY_QUIZZES_PER_PAGE)
        saved = Paginator(Game.objects.filter(creator=request.user, finished=True), MY_QUIZZES_PER_PAGE)
        owned = Paginator(Quiz.objects.filter(owner=request.user), MY_QUIZZES_PER_PAGE)
        running_page_number = request.GET.get('page_running') or 1
        saved_page_number = request.GET.get('page_saved') or 1
        owned_page_number = request.GET.get('page_owned') or 1
        return render(request, "quizzes/my_quizzes.html", {
            "title": "My quizzes",
            "running": running.get_page(running_page_number),
            "saved": saved.get_page(saved_page_number),
            "owned": owned.get_page(owned_page_number)
        })


@login_required(login_url='login', redirect_field_name=None)
def favourites_view(request):
    if request.method == "POST":
        quiz = Quiz.objects.get(id=request.POST["id"])
        if quiz.watching.filter(username=request.user.username).first():
            quiz.watching.remove(request.user)
        else:
            quiz.watching.add(request.user)
        return HttpResponseRedirect(reverse("quiz", kwargs={ 'id': request.POST["id"]}))
    else:
        paginator = Paginator(Quiz.objects.filter(watching=request.user), QUIZZES_PER_PAGE)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        return render(request, "quizzes/quizzes.html", {
            "title": "Favourites",
            "quizzes": paginator.get_page(page_number)
        })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "quizzes/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "quizzes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quizzes/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "quizzes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "quizzes/register.html")