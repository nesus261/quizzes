from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import User, Quiz, Question


QUIZZES_PER_PAGE = 10


def game_view(request, id):
    if request.method == "POST":
        pass
    else:
        quiz = Quiz.objects.get(id=id)
        return render(request, "quizzes/quiz.html", {
            "quiz": quiz,
            "questions": quiz.questions.all(),
            "favourite": quiz.watching.filter(username=request.user.username).first()
        })


def quiz_view(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, "quizzes/quiz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all(),
        "favourite": quiz.watching.filter(username=request.user.username).first()
    })


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
          quiz = Quiz(owner=request.user, title=title, category=category, description=description)
          quiz.save()
        except IntegrityError:
            return JsonResponse({
                "message": {
                    "title": "Error",
                    "body": "Title already taken"
                }
            }, status=201)
        for i in range(int(request.POST['questions_count'])):
            print(request.POST[f'query-{i}'])
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