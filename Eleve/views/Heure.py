from django.shortcuts import render,redirect
from django.contrib import messages
from Eleve.models import Disponibilite
from difflib import SequenceMatcher
def Heure_page(request):
    return render(request,'heure_ajout.html')
def Pop_None(liste):
    if None in liste :
        for num,valeur in enumerate(liste):
            if valeur == None:
                liste.pop(num)
        return liste
    else:
        return liste
def Enregistrement_heure(request):
    messages.warning(request,'La session n\'est pas post ok ?') if request.method != "POST" else True
    Debut = request.POST['Debut'] if request.POST['Debut'] != '' else False
    # doublons avec similarite eleve
    doublons = (False if len(Pop_None(list(set([x.Heure if SequenceMatcher(None,x.Heure,Debut).ratio() > 0.85 else None for x in Disponibilite.objects.all()]))))>=1 else True) if Debut else True
    enregistrement = Disponibilite(Heure=Debut)
    # enregistrement
    messages.warning(request,f'pas de input vide s\'il vous plait') if not Debut else True
    messages.warning(request,'Il existe dejas une heure comme celle-ci !') if not doublons else None

    enregistrement.save() if Debut and doublons else None
    return redirect('Heure')
