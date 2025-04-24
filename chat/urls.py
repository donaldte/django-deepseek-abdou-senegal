from django.urls import path 
from . import views

urlpatterns = [
    path('chat/<int:projet_id>/', views.ChatView.as_view(), name='chat'),
]
