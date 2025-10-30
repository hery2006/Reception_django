from django.urls import path
from .views import *
urlpatterns=[
    path('Professeur/main/page/',Prof_page_main,name='Prof_main'),
]