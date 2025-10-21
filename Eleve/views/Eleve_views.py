from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
def Eleve_fonctions(request):
    Donne_formations = Formations.objects.all()
    Donne_eleve = Eleve_class.objects.all() if 'rechercher' not in request.session else Eleve_class.objects.filter( Q(Nom__icontains=request.session['rechercher']['mot']) | Q(Prenom__icontains=request.session['rechercher']['mot']))
    session_Formations_eleve = {}

    for value in Donne_eleve:
        session_Formations_eleve[str(value.id)] = {}
        for formations_eleve in Formations_eleve.objects.filter(Eleve_choix=Eleve_class.objects.get(id = value.id)).all():
            session_Formations_eleve[str(value.id)][str(formations_eleve.Formations.Nom)] = {'id_formations':formations_eleve.id,
                    'Niveau':formations_eleve.Niveau,}
    request.session['avoir_le_bon_formations'] = session_Formations_eleve
    context = {
        'Formations':Donne_formations,
        'Eleve':Donne_eleve,
    }
    return render(request,'Eleve.html',context)

def Ajout_Eleve_fonctions(request):
    for x in range(1,7):
        if str(x) in request.session:
            del request.session[str(x)]
    if request.method != 'POST':
        return 
    Nom = request.POST['Nom'] if request.POST['Nom'] != '' else False
    Prenom = request.POST['Prenom'] if request.POST['Prenom'] != '' else False
    Droit = request.POST['Droit'] if request.POST['Droit'] != '' else False
    Dossier = request.POST['Dossier'] if request.POST['Dossier'] != '' else False
    Niveau = request.POST['Niveau']  if request.POST['Niveau'] != '' else False
    Formationss = Formations.objects.get(id = int(request.POST['Formations']))  if request.POST['Formations'] != '' else False
    Numero = request.POST['Numero'] if request.POST['Numero'] != '' else False
    messages.success(request,'Tous les champs doivent etre complet !') if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
    validator = False if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss or not Numero else True
    # effiter doublure de nom ou de prenom
    doublure = False if Eleve_class.objects.filter(Nom=Nom,Prenom=Prenom).exists() and int(Formationss.id) in [int(x.Formations.id) for x in Formations_eleve.objects.filter(Eleve_choix=Eleve_class.objects.get(Nom=Nom,Prenom=Prenom)).all()] else True
    messages.success(request,'Cette eleve excerce dejas la meme formations donc vous ne pouvez pas l\'ajouter. change le pour pouvoir le reenregistrer mercie ') if not doublure else True
    # avoir automatiquement le nombre de mois restant pour l'eleve selon le choix
    duree_formations = Formationss.duree if Formationss else False
    listage = [x.Niveaux for x in Niveau_Par_Formations.objects.filter(FK_formations = Formationss)] if Formationss else False
    valeur_final = []
    for num,value in enumerate(listage):
        if str(value) == str(Niveau) and listage and duree_formations and doublure:
            valeur_final.append( int(duree_formations - (num * (duree_formations/Formationss.level_number))))
    if validator and doublure:
        if not Eleve_class.objects.filter(Nom=Nom,Prenom=Prenom).exists():
            Ajout = Eleve_class(Nom=Nom,Prenom=Prenom,Droit=Droit,Dossier=Dossier,)
            Ajout.save()
        # Niveau=Niveau,Formations=Formationss,Reste_mois=valeur_final[0]
        Eleve_formations_ajout = Formations_eleve(Formations=Formationss,Niveau=Niveau,Reste_mois=valeur_final[0],Eleve_choix=Eleve_class.objects.get(Nom=Nom,Prenom=Prenom))
        Eleve_formations_ajout.save()
        request.session['user'] ={"id":Eleve_class.objects.get(Nom=Nom,Prenom=Prenom).id,
                                  "Formations_id":int(request.POST['Formations']),
                                  'Niveau':Niveau,
                                  'rowspan':Formationss.level_number + 1}
        # creations automatique de tous les mois ou il doit payer l'ecolage
        MOIS = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
        month_value = int(timezone.now().month) - 2
        stop = int(Formations_eleve.objects.get(Eleve_choix = Eleve_class.objects.get(Nom=Nom,Prenom=Prenom),Formations=Formationss).Reste_mois)
        Non_change_niveau = int((Formationss.duree/Formationss.level_number))
        stop_lost = 0
        liste_niveau = [ x.Niveaux for x in Niveau_Par_Formations.objects.filter(FK_formations = Formationss)]
        veritable = stop - Non_change_niveau
        Change_niveau = stop - veritable
        month_liste = []
        niveau_list = []
        while stop_lost < stop:
            stop_lost += 1
            month_value += 1
            if stop_lost == Change_niveau:
                take = int((stop_lost/Non_change_niveau))
                for x in range(Non_change_niveau):
                    niveau_list.append(liste_niveau[-take])
                Change_niveau += Non_change_niveau

            if month_value == 12:
                month_value = 0
            month_liste.append(MOIS[month_value])
        # renverser le liste pour avoir une liste croissante
        new_liste = []
        for x in range(stop):
            take_take = x + 1
            new_liste.append(niveau_list[-take_take])
        
        for numerotation,valuer_month in enumerate(month_liste):
            Mois_save = Mois_class(Nom=str(valuer_month),Eleve=Eleve_class.objects.get(Nom=Nom,Prenom=Prenom),Niveau=new_liste[numerotation],Formations=Formationss,Numero=Numero)
            Mois_save.save()
        return redirect('http://127.0.0.1:8000/Emplois_du_temps/')
    return redirect('http://127.0.0.1:8000/Eleve/')

def delete_eleve(request,id):
    Eleve_class.objects.get(id=id).delete()
    return redirect('http://127.0.0.1:8000/Eleve/')

def See_eleve(request,id,id_f):
    session = {}
    donne_eleve = Eleve_class.objects.get(id=id)
    donne_du_formations = Formations_eleve.objects.get(id=id_f)
    session['Eleve'] = {'id': id,
        "nom":donne_eleve.Nom,
        "Prenom":donne_eleve.Prenom,
        'Droit':donne_eleve.Droit,
        'Dossier':donne_eleve.Dossier,
        'Niveau':donne_du_formations.Niveau,
        "formations_id":donne_du_formations.Formations.id,
        'Activision':donne_eleve.Status,
        'id_f':id_f,
        'Numero':donne_eleve.Numero
    }
    Payement = Mois_class.objects.filter(Eleve = donne_eleve,Formations=int(donne_du_formations.Formations.id))
    context = {
        'Formations':Formations.objects.all(),
        'Payement':Payement,
    }
    # avoir l'emplois du temps personnel de chaque id 
    Session_emplois_du_temps = {}
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    Session_emplois_du_temps[str(donne_du_formations.Niveau)] = {}
    for value in Emplois_du_temps.objects.filter(Eleve = donne_eleve).all():
        Session_emplois_du_temps[str(donne_du_formations.Niveau)][str(jours[int(value.Jour_de_la_semaine) - 1])] = {'heure':value.Heure.Heure}


    request.session['personnel_emplois_du_temps'] = Session_emplois_du_temps
    request.session['user_take_eleve'] = session
    return render(request,'Eleve_See.html',context)

def Modifier_eleve_Donne(request,id):
    for x in range(1,7):
        if str(x) in request.session:
            del request.session[str(x)]
    if request.method != "POST":
        return 
    Nom = request.POST['Nom'] if request.POST['Nom'] != '' else False
    Prenom = request.POST['Prenom'] if request.POST['Prenom'] != '' else False
    Droit = request.POST['Droit'] if request.POST['Droit'] != '' else False
    Dossier = request.POST['Dossier'] if request.POST['Dossier'] != '' else False
    Niveau = request.POST['Niveau']  if request.POST['Niveau'] != '' else False
    Formationss = Formations.objects.get(id = int(request.POST['Formations']))  if request.POST['Formations'] != '' else False
    Activition = request.POST['Activision']
    Numero = request.POST['Numero'] if request.POST['Numero'] != '' else False
    messages.success(request,'Tous les champs doivent etre complet !') if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
    validator = False if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss or not Numero else True
    # effiter doublure de nom ou de prenom
    # Eviter changement Formations. valide que dans certains condition specifique
    # verifier si l'evele toujours actif 
    Actif_eleve = True if Eleve_class.objects.get(id=id).Status == True else False
    Verif_ecolage = True if Actif_eleve and len(list(set([x.Ecolage for x in Mois_class.objects.filter(Eleve = Eleve_class.objects.get(id=id))]))) == 1 else False
    doublure = False if Eleve_class.objects.filter(Nom=Nom,Prenom=Prenom).exists() and int(Formationss.id) in [int(x.Formations.id) for x in Formations_eleve.objects.filter(Eleve_choix=Eleve_class.objects.get(Nom=Nom,Prenom=Prenom)).all()] and Verif_ecolage  else True

    # verifier si eleve a payer tous les ecolage si il est actif sinon pas de changement de formations 
    verif_Formations = Verif_ecolage if Formationss.id != Formations_eleve.objects.get(Eleve_choix= Eleve_class.objects.get(id=id),Formations=Formationss).Formations.id else True

    messages.warning(request,f"Vous ne pouvez pas changer la formations tant que l'eleve n'a pas payer tous les ecolages") if not verif_Formations else True
    messages.success(request,'Cette eleve excerce dejas la meme formations donc vous ne pouvez pas le modifier. change le pour pouvoir le reenregistrer mercie ') if not doublure else True

    if not Verif_ecolage:
        Eleve_class.objects.filter(id=id).update(Status=Activition)
    if validator and doublure and Actif_eleve and verif_Formations:
        Ajout = Eleve_class.objects.filter(id=id).update(Nom=Nom,Prenom=Prenom,Droit=Droit,Dossier=Dossier,Status=Activition,Numero=Numero)
        request.session['user'] ={"id":id,
                                "Formations_id":int(request.POST['Formations']),
                                'Niveau':Niveau,
                                'rowspan':Formationss.level_number + 1}
        messages.success(request,'modification reussis avec success')



    messages.warning(request,f"Vous ne pouvez pas modifier les donnees de cette eleve car il n\'est Actif. Reactiver le pourvoir le remodifier mercie .") if not Actif_eleve and Activition != True else True

    return redirect(f'http://127.0.0.1:8000/See_Eleve/Https:8888%23/{request.session['user_take_eleve']['Eleve']['id']}/{request.session['user_take_eleve']['Eleve']['id_f']}')