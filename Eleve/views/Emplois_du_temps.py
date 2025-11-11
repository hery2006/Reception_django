from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
from typing import List,Dict,Set
import hashlib
JOURS = [str(x) for x in range(1,7)]
def emplois_du_temps(request,cles_unique:str):
    validator:bool = True if cles_unique != 'False' else False
    niveau = Niveau_Par_Formations.objects.filter(FK_formations = Formations.objects.get(id =request.session['user']['Formations_id'])).all() if not validator else Niveau_Par_Formations.objects.filter(FK_formations = Emplois_du_temps.objects.filter(cles_unique=cles_unique
    ).first().type_de_Formations.id).all()
    Payement = Mois_class.objects.filter(Eleve=Eleve_class.objects.get(id = request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).all() if not validator else False
    context = {
        'Disponibiliter':Disponibilite.objects.all(),
        'boucle_niveau':niveau,
        'Ecolage':Payement,
        'rowspan':request.session['user']['rowspan'] if not validator else len(niveau) + 1,
        'emplois': request.session.get('emplois_du_temps', {}),
        'cles_unique': cles_unique if validator else False
    }
    # print('ici mon gars ===>>',request.session['Jours_dejas_prise'])
    return render(request,'Emplois_du_temps.html',context)

def Creations_session_emplois(request,jours,heure,cles_unique:str):
    # creations de tuple qui peut contenir la totaliter de l'emplois du temps ici present
    validator:bool = True if cles_unique != 'False' else False
    id_last_Eleve = request.session['user']['id'] if not validator else False
    niveau = Niveau_Par_Formations.objects.get(FK_formations = Formations.objects.get(id =request.session['user']['Formations_id']),Niveaux = request.session['user']['Niveau']).Niveaux if not validator else Emplois_du_temps.objects.filter(cles_unique=cles_unique
    ).first().Niveau
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
    return redirect(f'http://127.0.0.1:8000/Emplois_du_temps/{cles_unique}/')

def cryptage_text(text:str)-> str:
    hachage = hashlib.sha384()

    hachage.update(text.encode("utf-8"))

    return hachage.hexdigest()

def Enregistrement_E_d_T(request):
    count = []
    liste_donnee:List[str] = []
    for jours in JOURS:
        if jours in request.session and request.session[jours]['id'] == request.session['user']['id']:
            count.append(jours)
            heure_append:str = request.session[jours]['heure']
            formations_id:str = request.session['user']['Formations_id']
            liste_donnee.append(str(jours))
            liste_donnee.append(heure_append)
            liste_donnee.append(formations_id)
    text_decodage = ''.join(str(x) for x in liste_donnee)

    cles_unique = cryptage_text(text_decodage)
    validator = False if int(len(count)) == int(Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations.cours_semaine) else True
    Evite_0 = False if len(count) == 0 else True
    messages.warning(request,f'le cours que vous avez choisis est disponible que {int(Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations.cours_semaine)} par semaine') if validator else None
    if not validator and Evite_0:
        for valeur in count:
            heure = Disponibilite.objects.get(Heure=request.session[str(valeur)]['heure'])
            Type_Formations = Formations_eleve.objects.get(Eleve_choix=Eleve_class.objects.get(id= request.session['user']['id']),Formations=Formations.objects.get(id =request.session['user']['Formations_id'])).Formations
            Eleve = Eleve_class.objects.get(id = int(request.session['user']['id']))
            save_value = Emplois_du_temps(Heure = heure,type_de_Formations = Type_Formations,Jour_de_la_semaine = f'{valeur}',Eleve=Eleve,Niveau=request.session['user']['Niveau'],cles_unique = cles_unique)
            save_value.save()
        # del request.session['user']
        for x in range(1,7):
            if str(x) in request.session:
                del request.session[str(x)]
        request.session['valid_ecolage'] = {'valid':True}
        
    return redirect(f'http://127.0.0.1:8000/Emplois_du_temps/{'False'}/')

def delete_session_emplois_temps(request,jours,cles_unique:str):
    validator = False if str(jours) in request.session else True

    messages.warning(request,"il n'y a rien a supprimer Monsieur le goat Herimanjato") if validator else True
    if not validator:
        del request.session[str(jours)]
    return redirect(f'http://127.0.0.1:8000/Emplois_du_temps/{cles_unique}/')