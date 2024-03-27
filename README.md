# Quiz portal

## Distinctiveness and Complexity

> My app is an app for creating and playing quizzes. It is significantly different from the other applications in the course and is not based on any previous project. It is also more complex than other projects in the course - it allows you to create, edit, and run quizzes that users can join via a browser. The project uses a websocket to create sessions of running quizzes.
> The project uses django on the back-end (and 6 django models: User, Quiz, Question, Game, Player, MarkedQuestion) and JavaScript on the front-end.
> The application is mobile-responsible.

## How to run application?

> Just run the commands below:
> git clone https://github.com/nesus261/quizzes.git
> cd quizzes
> pip install -r requirements.txt
> python manage.py runserver

## Project content

### Media

#### **media/profile_pictures**

> User profile photos.

#### **media/questions_images**

> Photos added to quiz questions.

### JavaScript

#### **quizzes/static/quizzes/script1.js**

> Client-side quiz creation. Responsible for managing questions in the quiz and sending a request to create a quiz to the server.

#### **quizzes/static/quizzes/script2.js**

> Responsible for opening quizzes when clicking on the container.

#### **quizzes/static/quizzes/script3.js**

> Responsible for the quiz page. Responsible for displaying the questions that the quiz contains and creating a quiz session that users can connect to.

#### **quizzes/static/quizzes/script4.js**

> Manages the admin page of the running quiz. Creates and maintains a websocket connection to the server, handles available quiz administrator actions on the website and displays players' progress.

#### **quizzes/static/quizzes/script5.js**

> Responsible for the quiz player's page. Creates and maintains a websocket connection to the server, handles player actions on the website, displays subsequent questions and the result after completing the quiz, along with selected answers (depending on the quiz settings).

#### **quizzes/static/quizzes/script6.js**

> Support for joining a quiz from the site navigator.

### Templates

#### **quizzes/templates/quizzes/add_quiz.html**

> Template for a website to create a quiz.

#### **quizzes/templates/quizzes/game_admin.html**

> Template for the admin page of a started/finished quiz.

#### **quizzes/templates/quizzes/game.html**

> Template for the player's page in the quiz.

#### **quizzes/templates/quizzes/layout.html**

> Website navigation template.

#### **quizzes/templates/quizzes/layout1.html**

> Template for the head of the page.

#### **quizzes/templates/quizzes/login.html**

> Template for the login page.

#### **quizzes/templates/quizzes/my_quizzes.html**

> Template for the my quizzes page. Displays saved, running and user-created quizzes.

#### **quizzes/templates/quizzes/quiz.html**

> Template for a quiz page. Displays information about the quiz and the settings for running the quiz for logged in users.

#### **quizzes/templates/quizzes/quizzes.html**

> Template for displaying a list of quizzes (home page, favorites).

#### **quizzes/templates/quizzes/register.html**

> Template for registration page.

### Python

#### **quiz_portal/routing.py**

> Websocket configuration.

#### **quizzes/templatetags/define_action.py**

> Support for useful python functions for templates.

#### **quizzes/admin.py**

> Access to models from the admin page.

#### **quizzes/consumers.py**

> Websocket server management - all actions performed on the server side in the running quiz.

#### **models.py**

> Models used: User, Quiz, Question, Game, Player, MarkedQuestion.

#### **views.py**

> Any server-side actions not performed using a websocket.

### CSS

### **quizzes/static/quizzes/style.css**

> Page styles.
