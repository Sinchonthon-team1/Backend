from django.db import models
from user.models import User

class Match (models.Model):
    teamName = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    matchDate = models.DateTimeField()
    teamScore = models.IntegerField()
    openChatUrl = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta : 
        db_table = "match"