from django.db import models
from user.models import User

# Create your models here.

class Team(models.Model):
    teamName = models.CharField(max_length=40)
    school = models.CharField(max_length=100)
    leader = models.ForeignKey(User, related_name='team_leader', on_delete=models.CASCADE)
    member2 = models.ForeignKey(User, related_name='team_member2', on_delete=models.CASCADE)
    member3 = models.ForeignKey(User, related_name='team_member3', on_delete=models.CASCADE)
    member4 = models.ForeignKey(User, related_name='team_member4', on_delete=models.CASCADE)
    member5 = models.ForeignKey(User, related_name='team_member5', on_delete=models.CASCADE)
    teamTier = models.IntegerField(default=0)

    class Meta : 
        db_table = 'teams'

