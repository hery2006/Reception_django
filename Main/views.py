from django.shortcuts import render
from Eleve.models import *
# Create your views here.
from django.contrib import messages


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
    emplois = Emplois_du_temps.objects.select_related('Heure', 'type_de_Formations').all()
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
                                              'nombre': len(list(set([ x.Eleve.id for x in emplois.filter(Heure=dispo,Jour_de_la_semaine=str(valeur),
                                              type_de_Formations = Formations.objects.get(Nom=str(name))).all()])))} for name in listeage]
            else:
                session_data[jour][heure] = "Libre"

    # Sauvegarder dans la session
    request.session['emplois_du_temps'] = session_data
    # print(request.session['emplois_du_temps'])
    # del request.session['emplois_du_temps']
    request.session['formations_table'] = tous_les_Formations
    # print(request.session['formations_table'])
    request.session.modified = True
def Voir_Emplois_du_temps(request,id,heure):
    donne_prendre_E_d_T = Formations_eleve.objects.filter(Formations = Formations.objects.get(id=id)).all()
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    # faire donc une boucle a L'horizentale

    session = {}
    len_colspan = {}
    Formations_name = {}
    Niveau = {}
    for value in donne_prendre_E_d_T:
        Eleve_donne = Eleve_class.objects.get(Nom=value.Eleve_choix.Nom,Prenom=value.Eleve_choix.Prenom,).Prenom
        session[Eleve_donne] = {}
        Niveau[Eleve_donne] = {'Prenom':Eleve_donne,
                           'Niveau':value.Niveau,
                           "heure":Emplois_du_temps.objects.filter(Eleve=Eleve_class.objects.get(Nom=value.Eleve_choix.Nom,Prenom=value.Eleve_choix.Prenom,),type_de_Formations=Formations.objects.get(id=id)).first().Heure.Heure}
        numbr = len([x.Jour_de_la_semaine for x in Emplois_du_temps.objects.filter(Eleve=Eleve_class.objects.get(Nom=value.Eleve_choix.Nom,Prenom=value.Eleve_choix.Prenom))])
        
        len_colspan['len'] = int(numbr)
        for valeur in Emplois_du_temps.objects.filter(Eleve=Eleve_class.objects.get(Nom=value.Eleve_choix.Nom,Prenom=value.Eleve_choix.Prenom),Heure=Disponibilite.objects.get(Heure = heure)):
            session[Eleve_donne][valeur.Jour_de_la_semaine] = {'Jours':jours[int(valeur.Jour_de_la_semaine) - 1]}
        request.session['voir'] = session
        request.session['niveau'] = Niveau
    print("voici le voir === >" ,request.session['voir'])
    New_len = len_colspan['len'] + 3
    Formations_name = {'title':Formations.objects.get(id=id).Nom,
                       'len':New_len,}
    request.session['title'] = Formations_name
    request.session['len_date'] = len_colspan
    
    context = {
        'donnee':donne_prendre_E_d_T,
        'valeur2':request.session['voir'],
        'id':id
    }
    return render(request,"Voir_E_d_T.html",context)

def modification_grouper_emplois_du_temps(request,id):
    pass