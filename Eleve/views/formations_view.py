from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone

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