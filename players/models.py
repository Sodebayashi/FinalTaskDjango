from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    gamename = models.CharField(max_length=100)
    
    def __str__(self):
        return self.gamename
    
class Player(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="players"
    )
    name = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    profile = models.TextField()
    achievement = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name