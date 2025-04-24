from django.db import models
from django.contrib.auth.models import User


class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
    
    
class ChatMessage(models.Model):
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    ai_response = models.TextField("AI Response", blank=True, null=True)

    def __str__(self):
        return self.contenu    