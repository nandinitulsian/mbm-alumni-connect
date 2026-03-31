from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'category', 'title', 'visibility', 'created_at']
    list_filter  = ['post_type', 'category', 'visibility']
    search_fields = ['author__full_name', 'title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_alumni_reply', 'created_at']
    list_filter  = ['is_alumni_reply']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    