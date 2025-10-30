# creation de fonctions capable de update
from django.shortcuts import render,redirect,HttpResponseRedirect
from Eleve.models import Formations_eleve,Emplois_du_temps,Eleve_class,Disponibilite
from django.contrib import messages
# pour emplois du temps
from typing import List,Dict
import hashlib
def cryptage_text(text:str)-> str:
    hachage = hashlib.sha384()

    hachage.update(text.encode("utf-8"))
    return hachage.hexdigest()
def Update_all(request,cles_unique:str,Eleve_number:int) ->render:
    JOURS:List[str] = [ str(x) for x in range(1,7)]
    jours_choices:List[str] = []
    change_cles_unique:List[str] = []
    for jours in JOURS:
        if jours in request.session:
            jours_choices.append(jours)
            heure_append:str = request.session[jours]['heure']
            formations_id:str = Emplois_du_temps.objects.filter(cles_unique=cles_unique).first().type_de_Formations.id
            change_cles_unique.append(str(jours))
            change_cles_unique.append(heure_append)
            change_cles_unique.append(formations_id)
    Conditionnement:bool = True if len(jours_choices) == Emplois_du_temps.objects.filter(cles_unique = cles_unique).first().type_de_Formations.cours_semaine else False
    messages.warning(request,f'Le cours en question ne depasse pas les {Emplois_du_temps.objects.filter(cles_unique = cles_unique).first().type_de_Formations.cours_semaine} pas semaine merci !') if Conditionnement else False
    jours_already_choice:List[str] = sorted(list(set([ i.Jour_de_la_semaine for i in Emplois_du_temps.objects.filter(cles_unique=cles_unique).all()])))
    text_decodage = ''.join(str(x) for x in change_cles_unique)
    new_cles_unique:str = cryptage_text(text_decodage)
    comptatibility:Dict = {}
    if Conditionnement:
        for cles,day in enumerate(jours_choices):
            comptatibility[str(day)] = Emplois_du_temps.objects.filter(cles_unique=cles_unique,Jour_de_la_semaine=jours_already_choice[cles]).update(Jour_de_la_semaine=str(day),Heure=Disponibilite.objects.get(Heure=request.session[str(day)]['heure']).id,cles_unique=new_cles_unique)
        return HttpResponseRedirect('http://127.0.0.1:8000/')
    return HttpResponseRedirect(f'http://127.0.0.1:8000/Emplois_du_temps/{cles_unique}/')
        