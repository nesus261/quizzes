# Quiz portal

## Distinctiveness and Complexity

My app is an app for creating and playing quizzes. It is My app is an app for creating and playing quizzes. It allows you to create, edit and run quizzes that users can join using a browser. The project uses a websocket to create sessions of triggered quizzes.
The project uses django on the back-end (and 6 django models: User, Quiz, Question, Game, Player, MarkedQuestion) and JavaScript on the front-end.
The application is mobile-responsible.

<ul>

### Challenges

#### Websocket communication

The most difficult part of the project was creating and operating a websocket server in Django. I had previously created projects using websocket servers in python and node.js, so I thought this was the best architecture for a quiz website - real-time communication, without constantly asking about changes on the server, and asynchronicity is a more efficient solution. So I was looking for a way to create a websocket server inside a django project and found the channels package that is suitable for this. Based on its documentation, I created files supporting the websocket server (routing.py and consumers.py) and configured django (settings.py file) to use it - I added channels to INSTALLED_APPS and configured asynchronous communication (ASGI). I also configured CHANNEL_LAYERS so that different socket instances can communicate with each other. I used channels.layers.InMemoryChannelLayer, which is not a good production solution, but is suitable for testing because I didn't want to install redis additionally (it doesn't work on windows, so I would have to use docker to make the project work independently of the operating system).  
I didn't have any problems with the client side because, as I mentioned above, I was already creating projects using websockets.

#### Templatetags

I noticed that it would be useful to be able to create variables in templates and I found a way to do it on the Internet - templatetags. I noticed that this is an easy way to use python functions from templates and I also used it, among others: to perform .all() and .count() on database objects directly from templates.

#### Sending csrf_token from JavaScript

To conveniently handle responses to sent queries, I send them via JavaScript fetch. To ensure security, I wanted to send csrf_token via JavaScript. For this purpose, I replace the onsubmit function with my own one, in which I send a fetch query providing the data taken from the form as body, which contains the generated csrf_token (new FormData(e.target)) and return false so as not to refresh the page.

</ul>

## How to run application?

Install git: https://git-scm.com/downloads  
Install python and pip: https://www.python.org/downloads/  
Run the commands below:

```
git clone https://github.com/nesus261/quizzes.git
cd quizzes
pip install -r requirements.txt
python manage.py runserver
```

## Project content

### Media

#### **media/questions_images**

> Photos added to quiz questions.

### JavaScript

#### **quizzes/static/quizzes/script1.js**

> Creating and modifying a quiz on the client side. Responsible for managing the questions in the quiz and sending a request to create or modify the quiz to the server.

#### **quizzes/static/quizzes/script2.js**

> Responsible for opening quizzes after clicking on the container and handling joining a quiz from the website navigator.

#### **quizzes/static/quizzes/script3.js**

> Responsible for the quiz page. Responsible for displaying the questions that the quiz contains and creating a quiz session that users can connect to.

#### **quizzes/static/quizzes/script4.js**

> Manages the admin page of the running quiz. Creates and maintains a websocket connection to the server, handles available quiz administrator actions on the website and displays players' progress.

#### **quizzes/static/quizzes/script5.js**

> Responsible for the quiz player's page. Creates and maintains a websocket connection to the server, handles player actions on the website, displays subsequent questions and the result after completing the quiz, along with selected answers (depending on the quiz settings).

### Templates

#### **quizzes/templates/quizzes/add_quiz.html**

> A template for a page for creating and modifying quizzes.

#### **quizzes/templates/quizzes/game_admin.html**

> Template for the admin page of a started/finished quiz. Shows players' progress.

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
