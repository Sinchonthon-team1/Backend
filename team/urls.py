from django.urls import path
from team.views import create_team, check_name, get_team

urlpatterns = [
    path('', create_team, name='create_team'),
    path('checkname/', check_name, name='check_name'),
    path('{str:id}/', get_team, name='get_team')
]