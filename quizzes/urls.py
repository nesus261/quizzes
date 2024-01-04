from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),

    path("add_quiz", views.add_quiz_view, name="add_quiz"),
    path("search", views.search_view, name="search"),
    path("favourites", views.favourites_view, name="favourites"),
    path("quiz/<int:id>", views.quiz_view, name="quiz"),
    path("category/<str:category>", views.category_view, name="category"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)