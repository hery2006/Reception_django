import re
import unicodedata
from difflib import get_close_matches, SequenceMatcher
from typing import List, Dict, Set, Optional
from Eleve.models import Formations,Niveau_Par_Formations
VOCAB = {
    "droit": "droit",
    "droits": "droit",
    "paye":True,
    "payer":True,
    'non':False,
    'dossier':'dossier',
    'dossie':'dossier',
    'pas':False,
    'formations':{},
    'actif':'Actif',
    'complet':True,
    'complets':True,
    'complete':True,
    'incomplet':False,
    'et':'et',
    'ou':'et',
    'plus':False,
}
# prochaine etape . faire une 
Vocabulaire:Set[str] = set()
for cles,valeur in VOCAB.items():
    Vocabulaire.add(cles)
def ajouter_autre_donnees(Data:Dict,new_items:Set[str]) -> Dict:
    All_formations = Formations.objects.all()
    for value in All_formations:
        Data.update({str(value.Nom).lower():str(value.Nom).lower()})
        new_items.add(str(value.Nom).lower())
    return Data,new_items
def Segmentation(text:str,Vocabulaire:Set[str],max_len:int = 40) -> List[str]:
    i = 0
    mot = text.strip()
    longeur = len(mot)
    resultat:List[str] = []
    while i < longeur:
        Ajouter = False
        for j in range(min(max_len + i,longeur),i,-1):
            mot_find = mot[i:j]
            if mot_find in Vocabulaire:
                resultat.append(mot_find)
                i = j
                Ajouter = True
                break
        if not Ajouter:
            i += 1
    return resultat
def Sentence_transformers(dictionnaire:Dict[str,str],Conditionnement:bool,Boucle:List,items_value:List[str]) ->Dict:
    final:Dict = {}
    for num,_ in enumerate(Boucle):
        phrase = dictionnaire[str(num)].split() + [str(Conditionnement)]
        print('voici tous les phrase pour voir',phrase)
        value = True if phrase.count('False') % 2 == 0 else False
        value2 = True if phrase.count("True") > 0 or phrase.count('True') == 0 else False
        final_value = True if value == value2 else False
        for num,valeur in enumerate(phrase):
            if valeur.lower() in items_value:
                final[valeur] = final_value
    return final
def Creation_regle_grammaticale(phrase:str,Vocab:Dict = VOCAB,items_list:List[str] = Vocabulaire) -> Dict:
    # creation simple de comprehesion de de phrase c'est a dire, comprendre la structure glogale d'une Phrase simple et une Phrase qui represente 2 ou plus de condition
    tr = phrase.lower()
    tr = unicodedata.normalize('NFKD',tr)
    tr = ''.join(v for v in tr if not unicodedata.combining(v))
    tr = re.sub(r',', ' et ', tr)
    tr = re.sub(r"[^a-z0-9\s]",'',tr)
    tr = re.sub(r'\s+',' ',tr).strip()
    ajouter_autre_donnees(VOCAB,new_items=Vocabulaire)
    # conditionnement du code.
    False_statue = True
    listage:List[str] = tr.split()
    longeur:int = len(listage)
    i = 0
    first_result:List[str] = []
    while i < longeur:
        mot = listage[i]
        for v,w in Vocab.items():
            if SequenceMatcher(None,v,mot).ratio() > 0.72 and len(v) == len(mot):
                first_result.append(str(w))
            if len(mot) > 7 and mot not in items_list:
                seg = Segmentation(mot,Vocabulaire)
                validation = True if len(seg) != 0 else False
                if validation :
                    for w in seg:
                        if w in Vocabulaire:
                            take:str = VOCAB[w]
                            first_result.append(take)
                        else:
                            pass 
        i += 1
    # les regles grammaticale majeur
    # pour une phrase simple ou avec plusieur conditionnement
    number_condition_and:int = first_result.count('et') if 'et' in first_result else False
    number_condition_or:int = first_result.count('ou') if 'ou' in first_result else False
    liste_condition:List[str] = ['et','ou']
    if len(first_result) > 0:
        if first_result[0] == 'False' :
            False_statue = False
            first_result.pop(0)
    nouvelle_phrase_simple = ' '.join(first_result)
    cles_used:List[int] = [0]
    separed_sentence:Dict =  {}
    if number_condition_and or number_condition_or:
        if number_condition_and:
            condition:str = liste_condition[0]
            len_max_phrase = len(nouvelle_phrase_simple)
            x = 0
            while x < (number_condition_and + 1):
                if len(cles_used) == 1:
                    first_place:int = nouvelle_phrase_simple.find(condition)
                    cles_used.append(first_place + 2)
                    pass
                separated = nouvelle_phrase_simple[sum(cles_used):len_max_phrase]
                new_cles:int = separated.find(condition)
                if len(cles_used) < number_condition_and + 1:
                    cles_used.append(new_cles + 2)
                x += 1
            for num,valeur in enumerate(cles_used):
                debut = cles_used[num] if num == 0 else cles_used[num] + cles_used[num - 1]
                fin = (debut + cles_used[num + 1] - 2 * (num if num != 0 else 1)) if len(cles_used) > num + 1 else len_max_phrase
                final_sentence = nouvelle_phrase_simple[debut:fin]
                separed_sentence[str(num)] = final_sentence
    if not number_condition_and:
        for num, _ in enumerate(cles_used):
            separed_sentence[str(num)] = f'{nouvelle_phrase_simple}'
    if len(first_result) >0:
        final = Sentence_transformers(separed_sentence,False_statue,cles_used,Vocabulaire)
    if len(first_result) == 0 :
        final:Dict = {'nom':tr}
    return final