from django.contrib import admin
from .models import Board, Card, Label, Comment, List


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'owner', 'is_public']
    search_fields = ['title', 'description']
    list_filter = ['is_public']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'list', 'priority']
    search_fields = ['title', 'description', 'list']


@admin.register(Label)
class LaberdAdmin(admin.ModelAdmin):
    list_display = ['title', 'board']
    search_fields = ['title', 'board']


@admin.register(List)
class LsitAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'created_at']
    search_fields = ['title', 'description', 'board']

