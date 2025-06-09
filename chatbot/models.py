from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.session_id} - {self.user.email if self.user else 'Anonymous'}"

class UserPreference(models.Model):
    IMPORTANCE_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    chat_session = models.OneToOneField(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    camera_importance = models.CharField(
        max_length=10,
        choices=IMPORTANCE_CHOICES,
        default='medium'
    )
    performance_needs = models.CharField(
        max_length=10,
        choices=IMPORTANCE_CHOICES,
        default='medium'
    )
    gaming_priority = models.CharField(
        max_length=10,
        choices=IMPORTANCE_CHOICES,
        default='low'
    )
    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Preferences for {self.chat_session}"
