from django.urls import path
from .views import *
urlpatterns=[
    path('',page_principales,name="homepage"),
    path('Voir_emplois_du_temps/<str:cles_unique>/',Voir_Emplois_du_temps,name='V_E_d_t'),
    path('update_emplois_du_temps/all/<str:cles_unique>/',modification_grouper_emplois_du_temps,name='update_EDP_Groupe'),
    path('Add_new/formations/<int:id>',Add_new_formations,name='Add_new_formations')
]