from django.contrib import admin
from .models import Projet, ChatMessage


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_creation', 'date_modification', 'createur')
    list_filter = ('date_creation', 'date_modification', 'createur')
    
    
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'date_creation', 'date_modification', 'createur', 'projet')
    list_filter = ('date_creation', 'date_modification', 'createur', 'projet')