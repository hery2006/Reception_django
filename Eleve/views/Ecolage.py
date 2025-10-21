from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
from django.contrib import messages
from django.utils import timezone
MOIS = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
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


def Modifier_ecolage(request):
    if request.session != 'POST':
        pass
    valeur = request.POST.getlist('ecolage_value')
    payer = request.POST.getlist('Validations_payement')
    validator = False if any(valeur) else True
    Mois_actuelle = MOIS[int(timezone.now().month) - 1]
    messages.warning(request,'Vous devez payer au moins une ecolage') if validator else True
    if not validator:
        for numero,value in enumerate(valeur):
            # print(value)
            if not validator and float(value) != 0:
                Payement = payer[numero]
                validator2 = True if Payement == 'False' else  False
                if not validator2:
                    Mois_class.objects.filter(id=int(Payement)).update(Ecolage=True,Ecolage_payer=float(value))
        messages.warning(request,'Vous devez valider le payement pour reussir la validations') if validator2 else True
        messages.success(request,"Enregistrement de l'eleve reussi avec success")
    return redirect(f'http://127.0.0.1:8000/See_Eleve/Https:8888%23/{request.session['user_take_eleve']['Eleve']['id']}/{request.session['user_take_eleve']['Eleve']['id_f']}')
