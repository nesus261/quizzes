# Quiz portal

## Distinctiveness and Complexity

> Moja aplikacja to aplikacja do tworzenia i grania w quizy. Znacząco różni się ona od innych aplikacji w kursie i nie jest oparta na żadnym poprzednim projekcie. Jest również bardziej złożona od innych projektów w kursie - pozwala na tworzenie, edytowanie i uruchamianie quizów, do których mogą dołączać użytkownicy za pomocą przeglądarki. Projekt korzysta z websocketu do tworzenia sesji uruchamianych quizów.
> Projekt używa django na back-endzie (i 6 modeli django: User, Quiz, Question, Game, Player, MarkedQuestion) i JavaScript na front-endzie.
> Aplikacja jest dostosowana do urządzeń mobilnych.

## How to run application?

>

## Project content

### Media

#### **media/profile_pictures**

> Zdjęcia profilowe użytkowników.

#### **media/questions_images**

> Zdjęcia dodane do pytań w quizach.

### JavaScript

#### **quizzes/static/quizzes/script1.js**

> Tworzenie quizu po stronie klienta. Obsługuje zarządzanie pytaniami w quizie i wysyłanie żadania utworzenia quizu do serwera.

#### **quizzes/static/quizzes/script2.js**

> Obsługa otwierania quizów po naciśnięciu na kontener.

#### **quizzes/static/quizzes/script3.js**

> Obsługa strony quizu. Obsługuje wyświetlanie pytań, które zawiera quiz i tworzenie sesji quizu, do której mogą podłączać się użytkownicy.

#### **quizzes/static/quizzes/script4.js**

> Obsługa strony administratora uruchomionego quizu. Tworzy i obsługuje połączenie websocket z serwerem, obsługuje dostępne akcje administratora quizu na stronie i wyświetla progress graczy.

#### **quizzes/static/quizzes/script5.js**

> Obsługa strony gracza quizu. Tworzy i obsługuje połączenie websocket z serwerem, obsługuje akcje gracza na stronie, wyświetla kolejne pytania i rezultat po zakończeniu quizu, razem z zaznaczonymi odpowiedziami (w zależności od ustawień quizu).

#### **quizzes/static/quizzes/script6.js**

> Obsługa dołączania do quizu z navigatora strony.

### Templates

#### **quizzes/templates/quizzes/add_quiz.html**

> Szablon strony do tworzenia quizu

#### **quizzes/templates/quizzes/game_admin.html**

> Szablon strony administratora uruchomionego/zakończonego quizu.

#### **quizzes/templates/quizzes/game.html**

> Szablon strony gracza w quizie.

#### **quizzes/templates/quizzes/layout.html**

> Szablon nawigacji strony.

#### **quizzes/templates/quizzes/layout1.html**

> Szablon dla head strony.

#### **quizzes/templates/quizzes/login.html**

> Szablon dla strony logowania.

#### **quizzes/templates/quizzes/my_quizzes.html**

> Szablon dla strony my quizzes. Wyświetla zapisane, uruchomione i utworzone przez użytkownika strony.

#### **quizzes/templates/quizzes/quiz.html**

> Szblon dla strony quizu. Wyświetla informacje o quizie oraz ustawienia uruchamianego quizu dla zalogowanych użytkowników.

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

> Obsługa serwera websocket - wszelkie akcje wykonywane po stronie serwera w uruchomionym quizie.

#### **models.py**

> Używane modele: User, Quiz, Question, Game, Player, MarkedQuestion.

#### **views.py**

> Wszelkie akcje po stronie serwera nie wykonywane za pomocą websocketu.

### CSS

### **quizzes/static/quizzes/style.css**

> Style strony.
