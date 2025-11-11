from django.shortcuts import render, redirect
from Eleve.models import *
from typing import *
from difflib import SequenceMatcher
from django.contrib import messages
import json
def Modules_pages(request,id:int) -> render:
    # le module choicis par le selectionneur
    Modules_choice = Formations.objects.get(id=id)
    All_level = Niveau_Par_Formations.objects.filter(FK_formations = Modules_choice).all()
    Session_modules:dict = {}
    donne_chart:List[int] = []
    for i in All_level:
        All_eleve:List = [ j for j in Formations_eleve.objects.filter(Formations = Modules_choice) if len(j.Niveau) == len(i.Niveaux) and SequenceMatcher(None,j.Niveau,i.Niveaux).ratio() > 0.9 and j.Eleve_choix.id in [ n.id for n in Eleve_class.objects.filter(Status = True)]]
        Session_modules[str(i.Niveaux)] = All_eleve
        donne_chart.append(len(All_eleve))
    chart_config = {
        'type':'bar',
        'data':{
            'labels':[i.Niveaux for i in All_level],
            'datasets':[{
                'labels':f'{Modules_choice.Nom}',
                'data':donne_chart,
                'borderWidth': 2,
            }],
            'options':{
                'responsive':True,
                'onClick':'chartClick',
            }
        }
    }
    
    context = {
        'Name':Modules_choice.Nom,
        'Boucle':Session_modules,
        'graphe':json.dumps(chart_config),
        'Module_id':id,
    }
    return render(request,'Module_pages.html',context)

def Next_level(request,Module_id:int,level_name:str) -> redirect:
    if request.method != 'POST':
        return redirect(f'http://127.0.0.1:8000/Modules/{Module_id}/see')
    Checked_student:List = request.POST.getlist(f'checkbox_{level_name}')
    # savoir si il y a vraiment une update ou pas
    All_level:List[str] = [ i.Niveaux for i in Niveau_Par_Formations.objects.filter(FK_formations=Module_id)]
    Index:int = All_level.index(level_name)
    Not_next_level:bool = True if Index == (len(All_level) - 1) and Checked_student != [] else False
    messages.warning(request,f'Il n\'y a plus de niveau apres {level_name}') if Not_next_level else False
    if not Not_next_level and All_level != []:
        for Eleve_id in Checked_student:
            key:int = Eleve_id
            New_level:str = All_level[Index + 1]
            Emplois_du_temps.objects.filter(Eleve = key,type_de_Formations = Module_id).update(Niveau = New_level )
            Formations_eleve.objects.filter(Eleve_choix = key,Formations = Module_id).update(Niveau = New_level)
    return redirect(f'http://127.0.0.1:8000/Modules/{Module_id}/see')