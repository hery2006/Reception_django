from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import re
import unicodedata
from difflib import get_close_matches, SequenceMatcher
from typing import List, Dict, Set, Optional
from .regle import Creation_regle_grammaticale
            

        


def recherche_fonctions_eleve(request):
    if request.method != 'POST' :
        return
    Phrase:str = request.POST['Recherche_text'].lower() if request.POST['Recherche_text'] != '' else False
    messages.success(request,'Entrer quelque chose a rechercher pas vide !') if not Phrase else True
    valeur:Dict = {}
    valeur = Creation_regle_grammaticale(Phrase) if Phrase else False
    if Phrase:
        request.session['rechercher'] = valeur
    else:
        if 'rechercher' in request.session:
            del request.session['rechercher']
    return redirect('Eleve_page')
    
