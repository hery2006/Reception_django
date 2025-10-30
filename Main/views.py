from django.shortcuts import render
from Eleve.models import *
# Create your views here.
from typing import Dict,List,Set
from django.contrib import messages
from .utilitaire import *

def page_principales(request):
    context = {
        'disponibiliter':Disponibilite.objects.all(),
        'emplois': request.session.get('emplois_du_temps', {}),
    }
    temps_F(request=request)
    # print(request.session['Lundi'])
    return render(request,"main.html",context)
def temps_F(request):
    # Récupérer les données
    emplois = Emplois_du_temps.objects.all()
    disponibilites = Disponibilite.objects.all()
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']

    # Structure principale
    session_data = {}
    listeage = []
    tous_les_Formations = {}
    for ji in Emplois_du_temps.objects.all():
        if ji.type_de_Formations.Nom not in listeage:
            listeage.append(ji.type_de_Formations.Nom)
    
    for x in listeage:
        tous_les_Formations[str(x)] = {}
    for num,jour in enumerate(jours):
        session_data[jour] = {}

        for dispo in disponibilites:
            heure = (dispo.Heure)
            valeur = num + 1
            # Filtrer si une formation correspond à ce jour et cette heure
            emploi_match = emplois.filter(
                Heure=dispo,
                Jour_de_la_semaine=str(valeur),
            ).first()
            if emploi_match:
                session_data[jour][heure] = [{str(name):str(name),
                                              'id':Formations.objects.get(Nom=str(name)).id,
                                              'cles_unique':Emplois_du_temps.objects.filter(type_de_Formations=Formations.objects.get(Nom = name).id).first().cles_unique,
                                              'nombre': len(list(set([ x.Eleve.id for x in emplois.filter(Heure=dispo,Jour_de_la_semaine=str(valeur),
                                              type_de_Formations = Formations.objects.get(Nom=str(name))).all()])))} for name in listeage]
            else:
                session_data[jour][heure] = "Libre"

    # Sauvegarder dans la session
    request.session['emplois_du_temps'] = session_data
    # print(request.session['emplois_du_temps'])
    request.session['formations_table'] = tous_les_Formations

    request.session.modified = True
def Voir_Emplois_du_temps(request,cles_unique:str) -> render:
    donnee_boucle = Emplois_du_temps.objects.filter(cles_unique=cles_unique)
    # creation de session tableau
    session_emplois:Dict[str,str] = {}
    Liste_personne:List[str] = []
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    
    for valeur in donnee_boucle:
        if valeur not in Liste_personne:
            Liste_personne.append(valeur.Eleve.id)
    colspan:List[int] = []
    for id_user in Liste_personne:
        nom = Eleve_class.objects.get(id = id_user).Prenom
        new_data =  Emplois_du_temps.objects.filter(cles_unique=cles_unique,Eleve=id_user)
        longeur:int = len([value for value in new_data])
        colspan.append(longeur)
        session_emplois[nom] = [{'heure':value.Heure.Heure,'jours':jours[int(value.Jour_de_la_semaine)-1],'Niveau':value.Niveau} for value in new_data]   

    context = {
        'emplois':session_emplois,
        'colspan':colspan[0],
        'cles_unique':cles_unique,
    }
    return render(request,"Voir_E_d_T.html",context)

def modification_grouper_emplois_du_temps(request,cles_unique:str)-> render:
    return Uptade_all.Update_all(request=request,cles_unique=cles_unique,Eleve_number=5)
    