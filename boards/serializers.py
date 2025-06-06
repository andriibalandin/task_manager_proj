from rest_framework import serializers
from .models import Label, Board, Comment, List, Card
from django.contrib.auth.models import User


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['id', 'title', 'board']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'card', 'created_at']


class CardSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    assigned_users = serializers.PrimaryKeyRelatedField(many=True,
        queryset=User.objects.all(),
        required=False)
    
    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'list', 'assigned_users', 'due_date', 'labels', 'comments' ,'order', 'created_at', 'updated_at', 'priority']


class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'description', 'board', 'order', 'cards', 'created_at']


class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)
    members = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'members', 'is_public', 'lists', 'created_at', 'updated_at']
