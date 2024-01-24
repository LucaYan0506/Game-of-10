from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    isGuest = models.BooleanField(default = False)

    def __str__(self):
        return self.username
    


class Game(models.Model):
    code = models.CharField(max_length = 10)
    board = models.CharField(max_length=200)
    creator_name = models.ForeignKey(User, related_name="createdGame", on_delete=models.CASCADE)
    player = models.ForeignKey(User, blank=True, null=True, related_name="joinedGame", on_delete=models.CASCADE)


