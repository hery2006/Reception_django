from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
# recherche simple
def recherche_fonctions_eleve(request):
    if request.method != 'POST' :
        return
    Post_nom_prenom = request.POST['Recherche_text'] if request.POST['Recherche_text'] != '' else False
    messages.success(request,'Entrer un nom ou un Prenom pour trouver la personne et non vide') if not Post_nom_prenom else True
    Listage = [ x for x in str(Post_nom_prenom)] if Post_nom_prenom != False else []
    Nom_ou_prenom = {}
    if Post_nom_prenom:
        Nom_ou_prenom = {'mot':Post_nom_prenom}
        request.session['rechercher'] = Nom_ou_prenom
    else:
        if 'rechercher' in request.session:
            del request.session['rechercher']
    return redirect('Eleve_page')

def divise_mot(liste_format):
    validator = True if len(liste_format) != 0 else False
    
