from django.shortcuts import render,redirect
from AppProf.models import *
from Eleve.models import *
from Main.models import *
from django.contrib import messages
import re,unicodedata
from difflib import SequenceMatcher
from typing import *
from django.utils import timezone
MOIS:List[str] = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
def Prof_page_main(request) -> render:
    Now_years:str = timezone.now().year
    Now_month:str = MOIS[timezone.now().month - 1]
    Actually_id_years = Annee_Class.objects.get(Annee = Now_years)
    Actually_month = Prof_Mois_payement.objects.get(Mois=Now_month,Years_reference = Actually_id_years)
    context = {
        "Formations":Formations.objects.all(),
        'Years_id':Actually_id_years.id,
        'Month_id':Actually_month.id,
    }
    return render(request,"Professeur.html",context)

def Prof_add_fonction(request) -> redirect:
    if request.method != 'POST':
        return redirect('http://127.0.0.1:8000/Professeur/main/page/')
    
    Nom = request.POST.get('Nom') if request.POST.get('Nom') != '' else False
    Prenom = request.POST.get('Prenom') if request.POST.get('Prenom') != '' else False
    Cin = request.POST.get('CIN') if request.POST.get('CIN') else False
    Formations_types = Formations.objects.get(id = int(request.POST.get('Formations'))) if request.POST.get('Formations') != '' else False
    Contrat = request.POST.get('Contrat') if request.POST.get('Contrat') != '' else False
    Payement = float(request.POST.get('Payement')) if request.POST.get('Payement') != '' else False

    messages.warning(request,'Il n\'y devrais pas avoir de champs vides merci') if not Nom or not Prenom or not Cin or not Formations_types or not Contrat or not Payement else True

    valid_conf:bool = False if not Nom or not Prenom or not Cin or not Formations_types or not Contrat or not Payement else True

    doublure:bool = Evite_doublure(request,Nom,Prenom ) if valid_conf else False

    Cin_valid = verif_Cin(request,Cin) if Cin else False
    if valid_conf and Cin_valid and doublure:
        Prof_status = Prof_models.objects.create(Nom=Nom,Prenom=Prenom,Cin=Cin_valid,Types_formation=Formations_types,Duree = Contrat,Payement=Payement)
        Prof_status.save()
    return redirect('http://127.0.0.1:8000/Professeur/main/page/')

def verif_Cin(request,text:str) -> str:
    reg = text.strip()
    reg = text.lower()
    reg = re.sub(r"[^a-z0-9\s]",' ',reg)
    reg = re.sub(r'\s+',' ',reg)
    print('voici le r ==>  ',reg,text)
    unique_bloc:str = re.sub(r' ','',reg)
    verif_len:int = len(unique_bloc)
    Format_liste:List[str] = reg.split()
    if verif_len != 12:
        messages.warning(request,'le CIN est invalide . veuiller verifier l\'ecriture ou autre chose')
        return False

    if len(Format_liste) != 1:
        # verifier si il sont par 3 
        liste_verif:List = [ x if len(x) == 3 else '' for x in Format_liste]
        validations:bool = all(liste_verif)
        messages.warning(request,'L\'ecriture du CIN comporte des erreurs corriger le pour etre valides. Merci') if not validations else True
        if validations:
            return reg.upper()
        return validations

    if len(Format_liste) == 1 :
        # separation du bloc par de espace
        words_by_words:List[str] = [ x for x in unique_bloc]
        words_by_words.insert(3,' ')
        words_by_words.insert(7,' ')
        words_by_words.insert(11,' ')
        return ''.join(x for x in words_by_words)

def Evite_doublure(request,Nom:str,Prenom:str) -> bool:
    Donnee:List[str] = []
    All_prof = Prof_models.objects.all()
    Phrase:str = " "
    for value in All_prof:
        if SequenceMatcher(None,value.Nom,Nom).ratio() > 0.82 and SequenceMatcher(None,value.Prenom,Prenom).ratio() > 0.82:
            Phrase:str = f'{value.Nom} {value.Prenom}'
            Donnee.append(Phrase)
            continue

    if len(Donnee) > 0:
        messages.warning(request,f'le Prof {Phrase} existe dejas dans la base de donne')
        return False
    return True

def Payement_pages(request,Years_id:int,Month_id:int) -> render:

    if Month_id == 0 :
        Now_month:str = MOIS[timezone.now().month - 1]
        Month_id = Prof_Mois_payement.objects.get(Mois=Now_month,Years_reference = Annee_Class.objects.get(id = Years_id)).id
    Prof_db = Prof_Paiement.objects.filter(years = Annee_Class.objects.get(id = Years_id),Mois = Prof_Mois_payement.objects.get(id = Month_id)).all()
    context = {'Annee':Annee_Class.objects.all(),
               'Mois':Prof_Mois_payement.objects.filter(Years_reference = Annee_Class.objects.get(id = Years_id)).all(),
               'PDB':Prof_db,
               'yid':Years_id,
               'mid':Month_id,}
    return render(request,'Prof_payement.html',context)

def Payement_pages_modif(request,PP:int) -> render:
    Prof_salary_choise = Prof_Paiement.objects.get(id = PP)
    context:Dict = {
        'Nom':f'{Prof_salary_choise.Prof_id.Prenom}',
        'PP_id':PP,
        'Work_day':Prof_salary_choise.Work_day,
        'Seance':Prof_salary_choise.Seance_Hours,
        'Status':Prof_salary_choise.Status,
        'Obs':Prof_salary_choise.Observations,
    }
    return render(request,'Effectuer_payement.html',context)

def Update_Payement(request,PP:int) -> redirect:
    if request.method != "POST":
        return ''
    # create a script able to update Prof_paiement models .
    total_day_work = request.POST.get('Work_day')
    hours_seance = request.POST.get('Seance_Hours')
    Observations = request.POST.get('Observations')
    Status:bool = request.POST.get('Status','')
    Verif_list:bool = all([total_day_work,hours_seance,Observations,Status])
    Avoid_hours:bool = (True if float(hours_seance) <= 0 else False) if Verif_list else False
    Avoid_day :bool = (True if float(total_day_work) <= 0 else False) if Verif_list else False

    messages.warning(request,'Vous devez completer a totaliter des inputs') if not Verif_list else True
    messages.warning(request,"Le nombre d'heure ne doit pas etre 0 ou un nombre inferieur a celle-ci") if Avoid_hours else True
    messages.warning(request,"Le nombre de jours de travail ne doit pas etre 0 ou un nombre inferieur a celle-ci") if Avoid_day  else True
    print(Verif_list,Avoid_day,Avoid_hours)
    Prof_donnee = Prof_Paiement.objects.get(id = PP)
    # part where we creat update code
    if Verif_list and not Avoid_day and not Avoid_hours:
        Salary_per_hours:float = Prof_donnee.Prof_id.Payement
        Total:float = float(total_day_work) * float(hours_seance) * Salary_per_hours
        Prof_Paiement.objects.filter(id = PP).update(Work_day = float(total_day_work),Seance_Hours = float(hours_seance),Total_Salary_month = Total,Observations = Observations,Status = Status)
        return redirect(f'http://127.0.0.1:8000/Payement_pages/redirect/{Prof_donnee.years.id}/{Prof_donnee.Mois.id}')
    return redirect(f'http://127.0.0.1:8000/Payement/status/{PP}/donnee/pages/')

def Prof_liste_pages(request) -> render:
    Prof_DB = Prof_models.objects.all()
    context = {
        'DB_prof':Prof_DB,
        'Formations':Formations.objects.all()
    }
    return render(request,'Prof_list.html',context)

def Update_donnees_prof_liste(request,id):
    if request.method != 'POST':
        return ''
    Nom = request.POST.get(f'Nom_{id}') if request.POST.get(f'Nom_{id}') != '' else False
    Prenom = request.POST.get(f'Prenom_{id}') if request.POST.get(f'Prenom_{id}') != '' else False
    Cin = request.POST.get(f'CIN_{id}') if request.POST.get(f'CIN_{id}') else False
    Formations_types = Formations.objects.get(id = int(request.POST.get(f'Formations_{id}'))) if request.POST.get(f'Formations_{id}') != '' else False
    Contrat = request.POST.get(f'Contrat_{id}') if request.POST.get(f'Contrat_{id}') != '' else False
    Status = request.POST.get(f'Status_{id}') if request.POST.get(f'Status_{id}') != '' else False
    Payement = float(request.POST.get(f'Payement_{id}')) if request.POST.get(f'Payement_{id}') != '' else False
    messages.warning(request,'Il n\'y devrais pas avoir de champs vides merci') if not Nom or not Prenom or not Cin or not Formations_types or not Contrat or not Payement else True

    valid_conf:bool = False if not Nom or not Prenom or not Cin or not Formations_types or not Contrat or not Payement else True

    # doublure:bool = Evite_doublure(request,Nom,Prenom ) if valid_conf else False

    Cin_valid = verif_Cin(request,Cin) if Cin else False
    if valid_conf and Cin_valid:
       Prof_models.objects.filter(id=id).update(Nom=Nom,Prenom=Prenom,Cin=Cin_valid,Types_formation=Formations_types,Duree = Contrat,Payement=Payement,Status = Status)
        
    return redirect('http://127.0.0.1:8000/Prof/List/all/')
