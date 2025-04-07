import json 
import ollama 
import markdown2 
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage, Projet


User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        """Connect to the WebSocket and join the chat room."""
        self.projet_id = self.scope['url_route']['kwargs']['projet_id']
        self.room_group_name = f'chat_{self.projet_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        """Disconnect from the WebSocket and leave the chat room."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data):
        """Receive a message from the WebSocket."""
        data = json.loads(text_data)
        user_message = data['message']
        
        # envoyer le message de l'utilisateur dans le project
        await self.send(text_data=json.dumps({"message": user_message, 'sender': 'user'}))
        
        # get the projet object
        project = await self.get_project(self.projet_id)
        
        if project is None:
            await self.send(text_data=json.dumps({"message": "Project not found.", 'sender': 'system'}))
            return
        
        # streaning model deepseek 
        
        ai_response = ''
        raw_markdown_response = ''
        
        stream = ollama.chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': user_message}],
            stream=True,
        )
        
        for chuck in stream:
            raw_markdown_response += chuck['message']['content']
            formatted_response = markdown2.markdown(raw_markdown_response)
            
            # envoie le message de l'IA dans le projet 
            await self.send(text_data=json.dumps({"message": formatted_response, 'sender': 'ai'}))
            await asyncio.sleep(0.05) # simulate a delay for streaming effect
            
        # sauvegarder le message de l'utilisateur et de l'IA dans la base de données
        await self.save_message(project, self.scope['user'], user_message, formatted_response)    
        
        # fermeture explicite de la connexion WebSocket et notification de l'utilisateur
        await self.send(text_data=json.dumps({"close": True, 'sender': 'system'}))  
        await self.close()  
                    
    
    @sync_to_async
    def get_project(self, projet_id):
        """Get the project object."""
        try:
            return Projet.objects.get(id=projet_id)
        except Projet.DoesNotExist:
            return None 
         
    @sync_to_async
    def save_message(self, project, user, user_message, ai_response):
        """Save the chat message to the database."""
        ChatMessage.objects.create(
            projet=project,
            createur=user,
            contenu=user_message,
            ai_response=ai_response
        )    
        
        
        
    