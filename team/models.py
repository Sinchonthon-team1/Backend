from django.db import models
from user.models import User


# Create your models here.

class Team(models.Model):
    teamName = models.CharField(max_length=40)
    school = models.CharField(max_length=500)
    leader = models.CharField(max_length=500)
    member2 = models.CharField(max_length=500)
    member3 = models.CharField(max_length=500)
    member4 = models.CharField(max_length=500)
    member5 = models.CharField(max_length=500)

    class Meta : 
        db_table = 'teams'

    def __str__(self):
        return self.teamName

