from django.shortcuts import render
from Eleve.models import *
from AppProf.models import *
# Create your views here.
from typing import Dict,List,Set
from django.contrib import messages
from .utilitaire import *
from django.utils import timezone
from .models import *
MOIS:List[str] = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']

def page_principales(request):
    Auto_create_Years_and_month()
    session_Niveau:dict = {}
    session_Nombre:dict = {}
    for i in Formations.objects.all():
        session_Niveau[str(i.id)] = {}
        session_Nombre[str(i.id)] = {'Nombre':len([j for j in Formations_eleve.objects.filter(Formations = i) if j.Eleve_choix.id in [ n.id for n in Eleve_class.objects.filter(Status = True)]])}
        for j in Niveau_Par_Formations.objects.filter(FK_formations = i.id).all():
            session_Niveau[str(i.id)][str(j.Niveaux)] = i.Ecolage
    context = {
        'disponibiliter':Disponibilite.objects.all(),
        'emplois': request.session.get('emplois_du_temps', {}),
        'Formations':Formations.objects.all(),
        'Niveau':session_Niveau,
        'Nombre':session_Nombre,
    }
    if 'Add_new' in request.session:
        del request.session['Add_new']
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
                                              'cles_unique':Emplois_du_temps.objects.filter(type_de_Formations=Formations.objects.get(Nom = name).id,Status = True).first().cles_unique,
                                              'nombre': len(list(set([ x.Eleve.id for x in emplois.filter(Heure=dispo,Jour_de_la_semaine=str(valeur),
                                              type_de_Formations = Formations.objects.get(Nom=str(name)),Status=True).all()])))} for name in listeage]
            else:
                session_data[jour][heure] = "Libre"

    # Sauvegarder dans la session
    request.session['emplois_du_temps'] = session_data
    # print(request.session['emplois_du_temps'])
    request.session['formations_table'] = tous_les_Formations

    request.session.modified = True

def Voir_Emplois_du_temps(request,cles_unique:str) -> render:
    donnee_boucle = Emplois_du_temps.objects.filter(cles_unique=cles_unique,Status=True)
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

def Add_new_formations(request,id:int) -> redirect:
    Donnee = Eleve_class.objects.get(id=id)
    session = {}
    session = {'Nom':Donnee.Nom,
               "Prenom":Donnee.Prenom,}
    request.session['Add_new'] = session
    messages.success(request,'Vous pouvez maintenant Ajouter une nouvelle Formations')
    return redirect('http://127.0.0.1:8000/Eleve/')

def Auto_create_Years_and_month() -> List:
    # creation automatique de Annee utiliser.
    Now_years:str = timezone.now().year
    Existance:bool = False if len(Annee_Class.objects.filter(Annee = Now_years)) > 0 else True
    if Existance:
        Annee_Class.objects.create(Annee = Now_years)
        print('annee bien cree motherfuck')
    # create month with the optimal years
    years_index = Annee_Class.objects.get(Annee = Now_years)
    Now_month:str = MOIS[timezone.now().month - 1]
    Month_Existance:bool = False if len(Prof_Mois_payement.objects.filter(Mois=Now_month,Years_reference=years_index))>0 else True
    if Month_Existance:
        Prof_Mois_payement.objects.create(Mois=Now_month,Years_reference=years_index)
    # create a list of Actif teacher for their Salary
    if len(Prof_models.objects.all()) > 0:
        id_liste:List[int] = [ value.id for value in Prof_models.objects.filter(Status = True).all()]
        # Now we will create take all inforamtion to complete all Modul called Prof_Paiement
        Month_index = Prof_Mois_payement.objects.get(Mois=Now_month,Years_reference=years_index)
        for j in id_liste:
        #     pass
            Prof_existance:bool = False if len(Prof_Paiement.objects.filter(Prof_id=Prof_models.objects.get(id = j),Mois = Month_index,years=years_index)) > 0 else True
            if Prof_existance:
                Prof_Paiement.objects.create(Prof_id=Prof_models.objects.get(id = j),Mois = Month_index,years=years_index)
    return []