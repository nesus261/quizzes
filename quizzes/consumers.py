import copy
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from django.db import IntegrityError
import re
from django.core import serializers
from asgiref.sync import sync_to_async

from .models import User, Quiz, Question, Game, Player, MarkedQuestion

        
class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.group_name = "game_%s" % self.game_id

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.admin = await self.check_creator_db() 
        self.marked = []

        await self.accept()
        await self.loadGame()
        
    async def loadGame(self):
        if self.admin:
            for user in await self.get_users_db():
                await self.send(json.dumps(
                    {
                        "type": "new_user",
                        "username": user["fields"]["name"],
                    }
                ))
            await self.send(json.dumps(
                {
                    "type": "quiz_data", 
                    "data": { "questions": await self.get_questions_db() } 
                }
            ))
            if await self.check_game_runing_db():
                await self.start_game()
            await self.send(json.dumps(
            {
                "type": "update_users",
                "data": await self.get_users_progress_db()
            }
        ))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if self.admin:
            if data["type"] == "remove_user":
                username = data["username"]
                await self.remove_user_db(username)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "remove_user",
                        "username": username,
                    },
                )
            elif data["type"] == "start_game":
                await self.start_game_db()
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "start_game"
                    },
                )
            elif data["type"] == "end_game":
                await self.end_game_db(save=False)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "end_game",
                        "save": False
                    },
                )
            elif data["type"] == "save_end_game":
                await self.end_game_db(save=True)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "end_game",
                        "save": True
                    },
                )
        else:
            if data["type"] == "answer":
                answer = data["answer"]
                excepted_answer = self.current_question.get("fields").get("answer")
                if re.search(f"^{excepted_answer}", answer):
                    result = True
                    self.rights += 1
                else:
                    result = False
                await self.mark_question_db(answer, result)
                self.progress += 1
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "update_users",
                        "data": { self.username: { "username": self.username, "progress": self.progress, "rights": self.rights } }
                    },
                )
                await self.next_question()

        if data["type"] == "new_user":
            username = data.get("username")
            user_id = data.get("id")
            new_user = await self.new_user_db(username, user_id)
            await self.set_init_results_db()
            if type(new_user) == list:
                new_user = new_user[0]
                if new_user == 4: # just id left from the previous quiz
                    pass
                elif new_user == 3:
                    await self.send(json.dumps(
                        {
                            "type": "Cannot join",
                            "reason": "Quiz is running"
                        }
                    ))
                elif new_user == 2:
                    await self.send(json.dumps(
                        {
                            "type": "user_id",
                            "data": user_id
                        }
                    ))
                    if await self.check_game_runing_db():
                        await self.start_game()
                elif new_user == 0:
                    await self.send(json.dumps(
                        {
                            "type": "error",
                            "reason": "Username already taken"
                        }
                    ))
            else:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "new_user",
                        "username": username,
                    },
                )
                await self.send(json.dumps(
                    {
                        "type": "user_id",
                        "data": new_user
                    }
                ))

    async def end_game(self, event):
        if not self.admin:
            return

        save = event["save"]
        if save:
            await self.send(json.dumps(
                {
                    "type": "save_end_game"
                }
            ))
        else:
            await self.send(json.dumps(
                {
                    "type": "end_game"
                }
            ))

    async def update_users(self, event):
        if not self.admin:
            return

        await self.send(json.dumps(
            {
                "type": "update_users",
                "data": event["data"],
            }
        ))
    
    async def start_game(self, event=None):
        if not hasattr(self, 'username') and not self.admin:
            return
        await self.send(json.dumps(
            {
                "type": "start_game"
            }
        ))
        await self.next_question()
    
    async def next_question(self):
        if self.admin:
            return
        next_question = await self.get_next_question_db()
        if next_question.get('end'):
            await self.send(json.dumps(
                {
                    "type": "end_quiz",
                    "data": await self.end_game_data_db()
                }
            ))
            return
        await self.send(json.dumps(
            {
                "type": "question",
                "data": {
                    "history": await self.get_marked_db(),
                    "current": next_question
                }
            }
        ))
    
    async def new_user(self, event):
        if not self.admin:
            return
        username = event["username"]

        await self.send(json.dumps(
            {
                "type": "new_user",
                "username": username,
            }
        ))

    async def remove_user(self, event):
        username = event["username"]
        if not self.admin:
            if hasattr(self, 'username') and username == self.username:
                await self.send(json.dumps(
                    {
                        "type": "user_removed"
                    }
                ), None, True)
            return

        await self.send(
            text_data=json.dumps(
                {
                    "type": "remove_user",
                    "username": username,
                }
            )
        )

    @sync_to_async
    def check_creator_db(self):
        try:
            self.game = Game.objects.get(code=self.game_id)
            return self.game.creator == self.scope["user"]
        except Game.DoesNotExist:
            raise DenyConnection("Invalid Chat Room")
        
    @sync_to_async
    def new_user_db(self, username, id):
        try:
            try:
                self.player = self.game.players.get(id=id)
                self.username = self.player.name
                return [2]
            except:
                if self.game.running:
                    return [3]
                try:
                    self.game.players.get(name=username)
                    return [0]
                except:
                    if username:
                        self.player = Player(game=self.game, name=username)
                        self.player.save()
                        self.username = self.player.name
                        return self.player.id
                    else:
                        return [4]
        except IntegrityError:
            return [0]
        
    @sync_to_async
    def set_init_results_db(self):
        self.results = [0, 0]
        try:
            self.progress = self.player.marked.all().count()
            self.rights = self.player.marked.filter(result=True).count()
        except IntegrityError:
            return [0]
        except AttributeError:
            self.progress = 0
            self.rights = 0
    
                    
    @sync_to_async
    def remove_user_db(self, username):
        try:
          self.game.players.get(name=username).delete()
          return True
        except IntegrityError:
            return False

    @sync_to_async
    def get_users_db(self):
        return json.loads(serializers.serialize("json", self.game.players.all()))
    
    @sync_to_async
    def start_game_db(self):
        self.game.running = True
        self.game.save()
    
    @sync_to_async
    def check_game_runing_db(self):
        return self.game.running
    
    @sync_to_async
    def get_questions_db(self):
        return json.loads(serializers.serialize("json", self.game.quiz.questions.all()))
    
    @sync_to_async
    def get_marked_db(self):
        return json.loads(serializers.serialize("json", self.player.marked.all()))
    
    @sync_to_async
    def mark_question_db(self, answer, result):
        marked_question = MarkedQuestion(player=self.player, game=self.game, question=self.game.quiz.questions.get(id=self.current_question.get("pk")), answer=answer, result=result)
        marked_question.save()
        self.marked.append(marked_question)
    
    @sync_to_async
    def get_users_progress_db(self):
        progress = {}
        for user in self.game.players.all():
            progress[user.name] =  { "username": user.name, "progress": user.marked.all().count(), "rights": user.marked.filter(result=True).count() }
        return progress
    
    @sync_to_async
    def end_game_data_db(self):
        data = { "rights": self.player.marked.filter(result=True).count(), "all": self.player.marked.all().count() }
        if self.game.show_player_answers:
            data["answers"] = []
            for question in self.player.marked.all():
                print(question.question.image)
                data["answers"].append({
                    "query": question.question.query,
                    "image": question.question.image if question.question.image else None,
                    "answer": question.answer,
                    "result": question.result,
                    "correct_answer": question.question.answer if self.game.show_correct_answers else None
                })
        return data

    @sync_to_async
    def get_next_question_db(self):
        try:
            question = json.loads(serializers.serialize("json", [list(self.game.quiz.questions.all())[self.player.marked.all().count()]]))[0]
            self.current_question = copy.deepcopy(question)
            del question["fields"]["answer"]
            return question
        except:
            return {"end": True}

    @sync_to_async
    def end_game_db(self, save):
        if save:
            self.game.finished = True
            self.game.save()
        else:
            self.game.delete()
    