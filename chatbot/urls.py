from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('widget/', views.get_chat_widget, name='widget'),
    path('message/', views.chat_message, name='message'),
]
