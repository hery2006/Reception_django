from django.shortcuts import render,redirect,get_object_or_404
from Eleve.models import *
from django.contrib import messages
from typing import *
MOIS:List[str] = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
def Enregistrement_ecolage(request):
    if request.session != 'POST':
        pass
    valeur = request.POST.getlist('ecolage_value')
    payer = request.POST.getlist('Validations_payement')
    Numero_fa = request.POST.getlist('Numero_fa')
    validator = False if any(valeur) else True
    print(valeur)
    messages.warning(request,'Vous devez payer au moins une ecolage') if validator else True
    if not validator:
        for numero,value in enumerate(valeur):
            # print(value)
            if not validator and value != '':
                Payement = payer[numero]
                Facture:str = Numero_fa[numero]
                print('id du valeur',Payement)
                validator2 = True if Payement == 'False' else  False
                print(validator2)
                if not validator2:
                    Mois_class.objects.filter(id=int(Payement)).update(Ecolage=True,Ecolage_payer=float(value),Numero_fa=Facture)
        messages.warning(request,'Vous devez valider le payement pour reussir la validations') if validator2 else True
        messages.success(request,"Enregistrement de l'eleve reussi avec success")
        if not validator2:
            del request.session['user']
            del request.session['valid_ecolage']
            return redirect('http://127.0.0.1:8000/Eleve/')

        # del request.session['nombre_niveau']
    return redirect(f'http://127.0.0.1:8000/Emplois_du_temps/{'False'}/')


def Modifier_ecolage(request):
    if request.session != 'POST':
        pass
    valeur = request.POST.getlist('ecolage_value')
    payer = request.POST.getlist('Validations_payement')
    Numero_fa = request.POST.getlist('Numero_fa')
    validator = False if any(valeur) else True
    messages.warning(request,'Vous devez payer au moins une ecolage') if validator else True
    if not validator:
        for numero,value in enumerate(valeur):
            Payement:str = payer[numero]
            Facture:str = Numero_fa[numero]
            # faire des changement de True en False
            mise_en_list:List[str] = Payement.split()
            if len(mise_en_list) > 1:
                verif_mois:bool = Mois_class.objects.get(id=int(mise_en_list[-1])).Ecolage
                if verif_mois == True:
                    Mois_class.objects.filter(id=int(mise_en_list[1])).update(Ecolage= False,Ecolage_payer=0,Numero_fa=Facture)
                else:
                    pass

            if not validator and float(value) != 0 and len(mise_en_list) == 1:
                    Mois_class.objects.filter(id=int(Payement)).update(Ecolage=True,Ecolage_payer=float(value),Numero_fa=Facture)
        messages.success(request,"Enregistrement de l'eleve reussi avec success")
    return redirect(f'http://127.0.0.1:8000/See_Eleve/Https:8888%23/{request.session['user_take_eleve']['Eleve']['id']}/{request.session['user_take_eleve']['Eleve']['id_f']}')

# ajouter une nouvelle mois en cas d'eleve recaler ou juste par besoins .
def Add_new_month(request,id:int) -> redirect:
    Niveau = request.POST.get('Niveau') if request.POST.get('Niveau') != '' else False
    month_number:int = int(request.POST.get('Month')) if request.POST.get('Month') != '' or request.POST.get('Month') == 0 else 1
    student = Eleve_class.objects.get(id=id)
    for x in range(month_number):
        last_month = Mois_class.objects.filter(Eleve = student).last()
        index_month:int = MOIS.index(last_month.Nom) + 1 if MOIS.index(last_month.Nom) != 11 else 0
        Mois_class.objects.filter(Eleve = student).create(Nom = MOIS[index_month],Formations = last_month.Formations,Niveau=Niveau,Eleve = student)
    return redirect(f'http://127.0.0.1:8000/See_Eleve/Https:8888%23/{id}/{request.session['user_take_eleve']['Eleve']['id_f']}')






