# Quiz portal

## Distinctiveness and Complexity

Moja aplikacja to aplikacja do tworzenia i grania w quizy. Pozwala ona na tworzenie, edytowanie i uruchamianie quizów, do których mogą dołączać użytkownicy za pomocą przeglądarki. Projekt korzysta z websocketu do tworzenia sesji uruchamianych quizów.  
Projekt używa django na back-endzie (i 6 modeli django: User, Quiz, Question, Game, Player, MarkedQuestion) i JavaScript na front-endzie.  
Aplikacja jest dostosowana do urządzeń mobilnych.

<ul>

### Wyzwania

#### Websocket communication

Najtrudniejsze w projekcie było utworzenie i obsługa serwera websocket w django. Wcześniej tworzyłem projekty korzystające z serwerów websocket w python i node.js, więc sądziłem, że to najlepsza architektura pod serwis z quizami - komunikacja w czasie rzeczywistym, bez odpytywania co chwilę o zmiany na serwerze i asynchroniczność są wydajniejszym rozwiązaniem. Szukałem więc możliwości utworzenia serwera websocket wewnątrz projektu django i znalazłem bibliotekę channels, która się do tego nadaje. Bazując na jej dokumentacji utworzyłem pliki obsługujące serwer websocket (routing.py i consumers.py) i skonfigurowałem django (plik settings.py) tak, by z niego korzystało - dodałem channels do INSTALLED_APPS i skonfigurowałem komunikację asynchroniczną (ASGI). Skonfigurowałem również CHANNEL_LAYERS, by różne instancje socketu mogły się ze sobą komunikować. Użyłem channels.layers.InMemoryChannelLayer, co nie jest dobrym rozwiązaniem produkcyjnym, ale nadaje się do testów, bo nie chciałem instalować dodatkowo redis (nie działa na windows, więc musiałbym użyć dockera, by projekt działał niezależnie od systemu operacyjnego).  
Nie miałem żadnych problemów ze stroną klienta, ponieważ, jak wspomniałem wyżej, tworzyłem już projekty korzystające z websocket.

#### Templatetags

Zauważyłem, że przydatna byłaby możliwość tworzenia zmiennych w templates i znalazłem w internecie sposób by to robić - templatetags. Zauważyłem, że to prosty sposób, by korzystać z funkcji pythona z templates i skorzystałem z niego również m.in. do wykonywania .all() i .count() dla obiektów z bazy danych bezpośrednio z templates.

#### Wysyłanie csrf_token z JavaScript

Aby wygodnie obsługiwać odpowiedzi na wysyłane zapytania, wysyłam je za pośrednictwem JavaScript fetch. By dbać o bezpieczeństwo chciałem wysyłać csrf_token przez JavaScript. W tym celu podmieniam funkcję onsubmit na własną, w której wysyłam zapytanie fetch podając jako body dane pobrane z formularza, które zawierają wygenerowany csrf_token (new FormData(e.target)) i zwracam false, by nie odświeżać strony.

</ul>

<br>

## How to run application?

Zainstaluj git: https://git-scm.com/downloads  
Zainstaluj python i pip: https://www.python.org/downloads/  
Uruchom poniższe komendy:

```
git clone https://github.com/nesus261/quizzes.git
cd quizzes
pip install -r requirements.txt
python manage.py runserver
```

## Project content

### Media

#### **media/questions_images**

> Zdjęcia dodane do pytań w quizach.

### JavaScript

#### **quizzes/static/quizzes/script1.js**

> Tworzenie i modyfikacja quizu po stronie klienta. Odpowiada za zarządzanie pytaniami w quizie i wysyłanie żądania utworzenia lub modyfikacji quizu do serwera.

#### **quizzes/static/quizzes/script2.js**

> Odpowiada za otwierania quizów po naciśnięciu na kontener oraz obsługę dołączania do quizu z navigatora strony.

#### **quizzes/static/quizzes/script3.js**

> Odpowiada za stronę quizu. Odpowiada za wyświetlanie pytań, które zawiera quiz i tworzenie sesji quizu, do której mogą podłączać się użytkownicy.

#### **quizzes/static/quizzes/script4.js**

> Zarządza stroną administratora uruchomionego quizu. Tworzy i obsługuje połączenie websocket z serwerem, obsługuje dostępne akcje administratora quizu na stronie i wyświetla progress graczy.

#### **quizzes/static/quizzes/script5.js**

> Odpowiada za stronę gracza quizu. Tworzy i obsługuje połączenie websocket z serwerem, obsługuje akcje gracza na stronie, wyświetla kolejne pytania i rezultat po zakończeniu quizu, razem z zaznaczonymi odpowiedziami (w zależności od ustawień quizu).

### Templates

#### **quizzes/templates/quizzes/add_quiz.html**

> Szablon dla strony do tworzenia i modyfikacji quizów.

#### **quizzes/templates/quizzes/game_admin.html**

> Szablon dla strony administratora uruchomionego/zakończonego quizu. Pokazuje progres graczy.

#### **quizzes/templates/quizzes/game.html**

> Szablon dla strony gracza w quizie.

#### **quizzes/templates/quizzes/layout.html**

> Szablon dla nawigacji strony.

#### **quizzes/templates/quizzes/layout1.html**

> Szablon dla head strony.

#### **quizzes/templates/quizzes/login.html**

> Szablon dla strony logowania.

#### **quizzes/templates/quizzes/my_quizzes.html**

> Szablon dla strony my quizzes. Wyświetla zapisane, uruchomione i utworzone przez użytkownika quizy.

#### **quizzes/templates/quizzes/quiz.html**

> Szablon dla strony quizu. Wyświetla informacje o quizie oraz ustawienia uruchamianego quizu dla zalogowanych użytkowników.

#### **quizzes/templates/quizzes/quizzes.html**

> Szablon dla wyświetlania listy quizów (strona główna, favourites).

#### **quizzes/templates/quizzes/register.html**

> Szablon dla strony rejestracji.

### Python

#### **quiz_portal/routing.py**

> Konfiguracja websocketu.

#### **quizzes/templatetags/define_action.py**

> Obsługa przydatnych funkcji w pythonie dla szablonów.

#### **quizzes/admin.py**

> Dostęp do modeli ze strony admina.

#### **quizzes/consumers.py**

> Zarządzanie serwerem websocket - wszelkie akcje wykonywane po stronie serwera w uruchomionym quizie.

#### **models.py**

> Używane modele: User, Quiz, Question, Game, Player, MarkedQuestion.

#### **views.py**

> Wszelkie akcje po stronie serwera nie wykonywane za pomocą websocketu.

### CSS

### **quizzes/static/quizzes/style.css**

> Style strony.
