from django.db import models

# Create your models here.
class Game(models.Model):
    code = models.CharField(max_length = 10)
    board = models.CharField(max_length=200)
    creator_name = models.CharField(max_length = 30)
    player2 = models.CharField(max_length = 30)