from django.urls import path
from AppProf.views import *
urlpatterns=[
    path('Professeur/main/page/',Prof_page_main,name='Prof_main'),
    path('Ajout/Prof/',Prof_add_fonction,name='Prof_add_urls'),
    path('Modules/<int:id>/see',Modules_pages,name='Modules_pages'),
    path('Next_level/<int:Module_id>/<str:level_name>/',Next_level,name='Pass_level'),
    path('Payement_pages/redirect/<int:Years_id>/<int:Month_id>',Payement_pages,name='Prof_payement'),
    path('Payement/status/<int:PP>/donnee/pages/',Payement_pages_modif,name='Pages_payement_modif'),
    path('Valid_prof/Payement/Valid/<int:PP>/',Update_Payement,name='Update_prof_p'),
    path('Prof/List/all/',Prof_liste_pages,name='Pages_liste'),
    path('update/<int:id>/valid_id/007',Update_donnees_prof_liste,name='Prof_update_liste')
]