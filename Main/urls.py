from django.urls import path
from .views import *
urlpatterns=[
    path('',page_principales,name="homepage"),
    path('Voir_emplois_du_temps/<int:id>/<str:heure>/',Voir_Emplois_du_temps,name='V_E_d_t')
]