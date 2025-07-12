
from django.contrib import admin
from .models import Skill, UserProfile, SwapRequest, Feedback, ChatMessage

# Show skills in admin
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# User Profile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'availability', 'is_public']
    search_fields = ['user__username', 'location']
    filter_horizontal = ['skills_offered', 'skills_wanted']

# Swap Request
@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'offered_skill', 'wanted_skill', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']

# Feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'rating', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']

# Chat Messages
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'swap', 'timestamp']
    search_fields = ['sender__username', 'message']
    list_filter = ['timestamp']
