from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    isGuest = models.BooleanField(default = False)

    def __str__(self):
        return self.username
    


class Game(models.Model):
    TURN_CHOICES = [
        (1, 'creator'),
        (2, 'player'),
    ]
    code = models.CharField(max_length = 10, primary_key=True)
    board = models.CharField(max_length=169, default=None, blank=True, null=True)
    creator_name = models.ForeignKey(User, related_name="createdGame", on_delete=models.CASCADE)
    creator_cards = models.CharField(max_length=10, default=None, blank=True, null=True)
    creator_score = models.IntegerField(default=0)
    player = models.ForeignKey(User, blank=True, null=True, related_name="joinedGame", on_delete=models.SET_NULL)
    player_cards = models.CharField(max_length=10,default=None, blank=True, null=True)
    player_score = models.IntegerField(default=0)
    turn = models.IntegerField(choices=TURN_CHOICES, default=1)
    lastMove = models.CharField(max_length=1000, default=None, blank=True, null=True)
    command = models.CharField(max_length=1000, default=None, blank=True, null=True)

