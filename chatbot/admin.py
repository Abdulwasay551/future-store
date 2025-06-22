from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ChatSession, UserPreference

# @admin.register(ChatSession)
# class ChatSessionAdmin(ModelAdmin):
#     list_display = ('session_id', 'user', 'created_at', 'updated_at')
#     search_fields = ('session_id', 'user__email')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(UserPreference)
# class UserPreferenceAdmin(ModelAdmin):
#     list_display = ('chat_session', 'camera_importance', 'performance_needs', 'gaming_priority', 'budget_min', 'budget_max')
#     list_filter = ('camera_importance', 'performance_needs', 'gaming_priority')
#     search_fields = ('chat_session__session_id', 'chat_session__user__email')
