from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    '''Board for organizing tasks'''
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class List(models.Model):
    '''List on the board'''
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title    


class Label(models.Model):
    '''Label for tasks categories'''
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return self.title


PRIORITY_CHOICES = [ 
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ] #priorities for cards

class Card(models.Model):
    '''Card for task in list'''

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='LOW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list_cards')
    assigned_users = models.ManyToManyField(User, related_name='asigned_cards')
    due_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    labels = models.ManyToManyField(Label, related_name='cards', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''Comment to card'''
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_comments')
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f'Comment by {self.author} on {self.card}'
    