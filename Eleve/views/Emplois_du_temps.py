from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
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