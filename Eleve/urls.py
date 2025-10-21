from django.urls import path
from .views import *
urlpatterns=[
    path('Formations/',Formations_views,name='Formations'),
    path('Enregistrement',Register,name='Register'),
    path('Del/<int:id>/',Delete_formations,name='delete_f'),
    path("Modifications/<int:id>",See_values,name='def_modif_f'),
    path('realisation',Update_values,name='modif_real'),
    # Eleve urls
    path('Eleve/',Eleve_fonctions,name='Eleve_page'),
    path('Ajout_eleve',Ajout_Eleve_fonctions,name='Ajout_html'),
    path('Del/<int:id>',delete_eleve,name="Delete_eleve"),
    path('niveau/',Niveau_formations,name='niveau'),
    path('See_Eleve/Https:8888#/<int:id>/<int:id_f>',See_eleve,name="See_eleve_urls"),
    path('Modifier_eleve/Forge_institute/<int:id>',Modifier_eleve_Donne,name='update_eleve_value'),
    path('recherche/mot/',recherche_fonctions_eleve,name='rechercher'),
    # urls Disponibilite
    path('Disponibilister',Heure_page,name='Heure'),
    path('Enregistrement/Disponibiliter/',Enregistrement_heure,name="heure_save"),
    # enregistrement ecolage
    path('Ecolage/enregistrement/',Enregistrement_ecolage,name='Ecolage_save'),
    path('Modification/Ecolage/',Modifier_ecolage,name='Modif_ecolage_state'),
    # emplois du temps
    path('Emplois_du_temps/',emplois_du_temps,name='E_d_T'),
    path("session_ET/<int:jours>/<str:heure>/",Creations_session_emplois,name="session"),
    path('Delete/<int:jours>/',delete_session_emplois_temps,name='delete_session_E_d_T'),
    path('enregistrement/Emplois_du_temps/',Enregistrement_E_d_T,name='enregistrement_E_d_T'),
]