from django.shortcuts import render, get_object_or_404
from .models import Projet, ChatMessage
from django.views import View


class ChatView(View):
    """View for the chat page."""

    def get(self, request, projet_id):
        """Handle GET requests to display the chat page."""
        projet = get_object_or_404(Projet, id=projet_id)
        messages = ChatMessage.objects.filter(projet=projet).order_by('-date_creation')
        return render(request, 'chat.html', {'projet': projet, 'messages': messages})
