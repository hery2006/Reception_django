# Nombre de ligne maximal pour ce views est de 600 pas plus.
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
#  -------------------------COTE FORMATIONS--------------------------------
def Formations_views(request):
    # prendre tous les informations dans le module Formations
    v_formations = Formations.objects.all()
    valeur_range = range(int(request.session['nombre_niveau']['nombre'])) if 'nombre_niveau' in request.session else None
    context = {
        'Formations':v_formations,
        'range_format': valeur_range if valeur_range != None else [],
    }
    
    return render(request,'Formations.html',context)

def Register(request):
    # enregistrement des Formations
    if request.method != 'POST':
        return ''
    v_nom = request.POST['nom']
    v_Duree = request.POST['Duree']
    v_level = request.POST['level']
    v_ecolage = request.POST['Ecolage']
    v_type_formations = request.POST['Type_Formations']
    v_cours = request.POST['cours_semaine']

    validator = False if v_Duree == '' or v_nom == '' or v_level == '' or v_ecolage == '' or v_type_formations == '' or v_cours == '' else True

    messages.success(request,f'il y a des champs vide !') if v_Duree == '' or v_nom == '' or v_level == '' or v_ecolage == '' or v_type_formations == '' or v_cours == '' else None
    # savoir si c'est une update ou une enregistrement
    liste_Formations = list(set([answer.Nom if SequenceMatcher(None,v_nom.lower(),answer.Nom.lower()).ratio() > 0.7 else None for answer in Formations.objects.all()]))
    for value in liste_Formations:
        if value != None and validator == True:
            id_taked = Formations.objects.get(Nom=value).pk
            return Evite_double(request=request,value=id_taked)

    if validator == True and len(liste_Formations) < 2:
        enregistrement = Formations(Nom = v_nom,duree = int(v_Duree),level_number = int(v_level),Ecolage =v_ecolage,Type_Formations = v_type_formations,cours_semaine = int(v_cours))
        enregistrement.save()
        request.session['nombre_niveau'] = {'nombre':int(v_level),
                                            'valid':True,
                                            'id_du_for':Formations.objects.get(Nom = v_nom).id,}
    return HttpResponseRedirect('Formations/')

def Evite_double(request,value):
    Title = Formations.objects.get(id=value).Nom
    messages.warning(request,f"La Formation '{Title}' existe dejas !")
    return HttpResponseRedirect('Formations/')

def Delete_formations(request,id):
    Formations.objects.filter(id=id).delete()
    return redirect('http://127.0.0.1:8000/Formations/')

def See_values(request,id):
    Nom = get_object_or_404(Formations,id=id).Nom
    Duree = get_object_or_404(Formations,id=id).duree
    Niveau = get_object_or_404(Formations,id=id).level_number
    Ecolage = get_object_or_404(Formations,id=id).Ecolage
    Type_formations = get_object_or_404(Formations,id=id).Type_Formations
    liste_tuplage = {
        'nom':Nom,
        'Duree':Duree,
        'Niveau':Niveau,
        'Ecolage':Ecolage,
        'Type_formations':Type_formations,
        'cours_semaine':get_object_or_404(Formations,id=id).cours_semaine,
    }
    request.session['valide_modif_f'] = liste_tuplage
    request.session['valide_t_f'] = {'True':True}
    # messages.warning(request,f'{request.session['valide_modif_f']}')
    return redirect('http://127.0.0.1:8000/Formations/')

def Update_values(request):
    if request.method != 'POST':
        return ''
    v_cours = request.POST['cours_semaine']
    v_nom = request.POST['nom']
    v_Duree = request.POST['Duree']
    v_level = request.POST['level']
    v_ecolage = request.POST['Ecolage']
    v_type_formations = request.POST['Type_Formations']
    # prendre l'id du nom ajouter par l'utilasateur
    validator = False if v_Duree == '' or v_nom == '' or v_level == '' or v_ecolage == '' or v_type_formations == '' or v_cours == '' else True
    messages.success(request,f'il y a des champs vide !') if v_Duree == '' or v_nom == '' or v_level == '' or v_ecolage == '' or v_type_formations == '' or v_cours == '' else None
    update = Formations.objects.filter(Nom=v_nom).update(Nom = v_nom,duree = int(v_Duree),level_number = int(v_level),Ecolage =v_ecolage,Type_Formations = v_type_formations,cours_semaine = int(v_cours)) if validator else True
    # prendre comme meme la modification meme si le nom est changer par autre chose ou je sais pas quoi !
    if not update:
        new_update = list(set([answer.Nom if SequenceMatcher(None,v_nom.lower(),answer.Nom.lower()).ratio() > 0.7 else None for answer in Formations.objects.all()]))
    def pop_None(liste):
        if len(liste) > 1:
            for numero, valeur in enumerate(liste):
                if valeur == None:
                    liste.pop(numero)
                    return liste    
        else:
            return liste
    nouveau_nom = pop_None(new_update) if not update else False

    if nouveau_nom and len(nouveau_nom) == 1:
        Formations.objects.filter(Nom=nouveau_nom[0]).update(Nom = v_nom,duree = int(v_Duree),level_number = int(v_level),Ecolage =v_ecolage,Type_Formations = v_type_formations,cours_semaine = int(v_cours))
        valid_niveaux = True if int(v_level) != int(Niveau_Par_Formations.objects.filter(FK_formations=Formations.objects.get(Nom = v_nom)).count()) else False
        if valid_niveaux:
            Niveau_Par_Formations.objects.filter(FK_formations=Formations.objects.get(Nom = v_nom)).delete()
            request.session['nombre_niveau'] = {'nombre':int(v_level),
                                                'valid':True,
                                                'id_du_for':Formations.objects.get(Nom = v_nom).id,}
            messages.success(request,f"Enregistrement reussis")
    if update:
        valid_niveaux = True if int(v_level) != int(Niveau_Par_Formations.objects.filter(FK_formations=Formations.objects.get(Nom = v_nom)).count()) else False
        if valid_niveaux:
            Niveau_Par_Formations.objects.filter(FK_formations=Formations.objects.get(Nom = v_nom)).delete()
            request.session['nombre_niveau'] = {'nombre':int(v_level),
                                                'valid':True,
                                                'id_du_for':Formations.objects.get(Nom = v_nom).id,}
            messages.success(request,f"Enregistrement reussis")

    if nouveau_nom and len(nouveau_nom) == 0 :
        messages.success(request,f"vous devez faire une enregistrement et non une modification")
    request.session['valide_t_f'] = {'True':False}
    return redirect('http://127.0.0.1:8000/Formations/')

def Niveau_formations(request):
    if request.method != 'POST':
        return None
    niveau = request.POST.getlist('Niveaux')
    validator = False if not all(niveau) else True 
    messages.warning(request,f'il faut completer la totalite de tous les niveau') if not validator else True
    Formations_table = Formations.objects.get(id=int(request.session['nombre_niveau']['id_du_for'])) if 'nombre_niveau' in request.session else False
    if validator and Formations_table:
        for value in niveau:
            Niveau_save = Niveau_Par_Formations(FK_formations=Formations_table,Niveaux=value)
            Niveau_save.save()
        del request.session['nombre_niveau']
        return redirect('http://127.0.0.1:8000/Formations/')

    return redirect('http://127.0.0.1:8000/Formations/')
# -----------------------FIN DE VIEWS FORMATIONS---------------------------


# ---------------------------COTE ELEVE------------------------------------
def Eleve_fonctions(request):
    Donne_formations = Formations.objects.all()
    Donne_eleve = Eleve_class.objects.all()
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
    messages.success(request,'Tous les champs doivent etre complet !') if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
    validator = False if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
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
            Mois_save = Mois_class(Nom=str(valuer_month),Eleve=Eleve_class.objects.get(Nom=Nom,Prenom=Prenom),Niveau=new_liste[numerotation],Formations=Formationss)
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

    messages.success(request,'Tous les champs doivent etre complet !') if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
    validator = False if not Nom or not Prenom or not Droit or not Dossier or not Niveau or not Formationss else True
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
        Ajout = Eleve_class.objects.filter(id=id).update(Nom=Nom,Prenom=Prenom,Droit=Droit,Dossier=Dossier,Status=Activition)
        request.session['user'] ={"id":id,
                                "Formations_id":int(request.POST['Formations']),
                                'Niveau':Niveau,
                                'rowspan':Formationss.level_number + 1}
        messages.success(request,'modification reussis avec success')



    messages.warning(request,f"Vous ne pouvez pas modifier les donnees de cette eleve car il n\'est Actif. Reactiver le pourvoir le remodifier mercie .") if not Actif_eleve and Activition != True else True

    return redirect(f'http://127.0.0.1:8000/See_Eleve/Https:8888%23/{request.session['user_take_eleve']['Eleve']['id']}/{request.session['user_take_eleve']['Eleve']['id_f']}')
# ----------------------FIN COTE ELEVE ------------------------------------


# ------------------------COTE EMPLOIS DU TEMPS ---------------------------
JOURS = [str(x) for x in range(1,7)]
def emplois_du_temps(request):
    niveau = Niveau_Par_Formations.objects.filter(FK_formations = Formations.objects.get(id =request.session['user']['Formations_id'])).all()
    Payement = Mois_class.objects.filter(Eleve=Eleve_class.objects.get(id = request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).all()
    # creations session pour voir tous les heure dejas prise ou pas
    Session_E_d_T = {}
    for value in JOURS:
        Session_E_d_T[str(value)] = {}
        for dispo in Disponibilite.objects.all():
            if Emplois_du_temps.objects.filter(Heure = dispo).count() != 0 and Emplois_du_temps.objects.filter(Jour_de_la_semaine=str(value)):
                listage_niveau = list(set([ x.Niveau for x in Emplois_du_temps.objects.filter(Heure = dispo).all()]))
                Session_E_d_T[str(value)][str(dispo.Heure)] = {}
                for value2 in listage_niveau:
                    Session_E_d_T[str(value)][str(dispo.Heure)][str(value2)] = {
                        'total':len(list(set([x.Eleve.Prenom for x in Emplois_du_temps.objects.filter(Heure = dispo,Niveau=str(value2))])))
                    }
            else:
                Session_E_d_T[str(value)][str(dispo.Heure)] = {'Libre':'Libre'}

    request.session['Jours_dejas_prise'] = Session_E_d_T
    context = {
        'Disponibiliter':Disponibilite.objects.all(),
        'boucle_niveau':niveau,
        'Ecolage':Payement,
        'Dejas_Prise':request.session['Jours_dejas_prise']
    }
    print('ici mon gars ===>>',request.session['Jours_dejas_prise'])
    return render(request,'Emplois_du_temps.html',context)

def Creations_session_emplois(request,jours,heure):
    # creations de tuple qui peut contenir la totaliter de l'emplois du temps ici present
    id_last_Eleve = request.session['user']['id']
    niveau = Niveau_Par_Formations.objects.get(FK_formations = Formations.objects.get(id =request.session['user']['Formations_id']),Niveaux = request.session['user']['Niveau']).Niveaux
    jours_tuple = {"id":id_last_Eleve,
        'Niveau_session':str(niveau),
        'heure':heure,
        str(jours):{
        "Choisis":False,
        "validite":"Choisis"
        }}
    jours_tuple[str(jours)]['Choisis'] = True
    # validator = False if str(jours) in request.session else True
    request.session[str(jours)] = jours_tuple
    return redirect('http://127.0.0.1:8000/Emplois_du_temps/')

def Enregistrement_E_d_T(request):
    count = []
    for jours in JOURS:
        if jours in request.session and request.session[jours]['id'] == request.session['user']['id']:
            count.append(jours)
    validator = False if int(len(count)) == int(Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations.cours_semaine) else True
    Evite_0 = False if len(count) == 0 else True

    messages.warning(request,f'le cours que vous avez choisis est disponible que {int(Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations.cours_semaine)} par semaine') if validator else None
    if not validator and Evite_0:
        for valeur in count:
            heure = Disponibilite.objects.get(Heure=request.session[str(valeur)]['heure'])
            Type_Formations = Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations
            Eleve = Eleve_class.objects.get(id = int(request.session['user']['id']))
            save_value = Emplois_du_temps(Heure = heure,type_de_Formations = Type_Formations,Jour_de_la_semaine = f'{valeur}',Eleve=Eleve,Niveau=request.session['user']['Niveau'])
            save_value.save()
        # del request.session['user']
        for x in range(1,7):
            if str(x) in request.session:
                del request.session[str(x)]
        request.session['valid_ecolage'] = {'valid':True}
        
    return redirect('http://127.0.0.1:8000/Emplois_du_temps/')

def delete_session_emplois_temps(request,jours):
    validator = False if str(jours) in request.session else True

    messages.warning(request,"il n'y a rien a supprimer Monsieur le goat Herimanjato") if validator else True
    if not validator:
        del request.session[str(jours)]
    return redirect('http://127.0.0.1:8000/Emplois_du_temps/')
# -----------------------FIN COTE EMPLOIS DU TEMPS-------------------------

# ----------------------------COTE ECOLAGE--------------------------------
def Enregistrement_ecolage(request):
    if request.session != 'POST':
        pass
    valeur = request.POST.getlist('ecolage_value')
    payer = request.POST.getlist('Validations_payement')
    validator = False if any(valeur) else True
    print(valeur)
    messages.warning(request,'Vous devez payer au moins une ecolage') if validator else True
    if not validator:
        for numero,value in enumerate(valeur):
            # print(value)
            if not validator and value != '':
                Payement = payer[numero]
                print('id du valeur',Payement)
                validator2 = True if Payement == 'False' else  False
                print(validator2)
                if not validator2:
                    Mois_class.objects.filter(id=int(Payement)).update(Ecolage=True,Ecolage_payer=float(value))
        messages.warning(request,'Vous devez valider le payement pour reussir la validations') if validator2 else True
        messages.success(request,"Enregistrement de l'eleve reussi avec success")
        if not validator2:
            del request.session['user']
            del request.session['valid_ecolage']
            return redirect('http://127.0.0.1:8000/Eleve/')

        # del request.session['nombre_niveau']
    return redirect('http://127.0.0.1:8000/Emplois_du_temps/')
    
#  ----------------------------FIN-----------------------------------------
def recherche_fonctions(request):
    pass