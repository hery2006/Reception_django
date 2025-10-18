# # from difflib import SequenceMatcher

# # print(SequenceMatcher(None,'niveau 1','Niveau 1').ratio())
# # x= 12
# # y=4

# # z = x/y
# # listage = ['x','y','z','y']

# # for num,val in enumerate(listage):
# #     if str(val) == 'y':
# #         val_n = x - ((num) * z)
# #         print(val_n,'nombre niveau :',z)


# # FAIRE UNE INCREMENTATION ET REVENIR A 0 UNE FOIS UNE NOMBRE DONNE 
# MOIS = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
# start = 0
# value = 10 - 2
# stop_value = 8
# non_change_niveau = 4
# month_liste = []
# veritable = stop_value - non_change_niveau
# change_niveau =  stop_value - veritable
# niveau = []
# valid_take = ['Niveau A1','Niveau A2','Niveau B1']
# while start < stop_value:
#     start += 1
#     value += 1
#     # print(start)
#     # print('change nivau',change_niveau)
#     if start == change_niveau:
#         take = int((start/non_change_niveau))
#         # print('voici le take ',take)
#         # print('le change niveau change de',change_niveau)
#         for x in range(non_change_niveau):
#             niveau.append(valid_take[-take])
#         # print(change_niveau)
#         change_niveau += non_change_niveau
#     if value == 12:
#         value = 0

#     month_liste.append(MOIS[value])


# new_liste = []

# for x in range(stop_value):
#     take = x + 1
#     new_liste.append(niveau[-take])

# print(new_liste)


liste = [ f"liste_{x}" for x in range(5)] 
print(liste)
{'Lundi': {'8h - 10h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': ['niveau A1'], 'total_eleve': 5, 'donne_necessaire': 1}}, '10h - 12h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': [], 'total_eleve': 1, 'donne_necessaire': 1}}, '14h - 16h': 'Libre'}, 'Mardi': {'8h - 10h': 'Libre', '10h - 12h': 'Libre', '14h - 16h': 'Libre'}, 'Mercredi': {'8h - 10h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': ['niveau A1'], 'total_eleve': 5, 'donne_necessaire': 1}}, '10h - 12h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': [], 'total_eleve': 1, 'donne_necessaire': 1}}, '14h - 16h': 'Libre'}, 'Jeudi': {'8h - 10h': 'Libre', '10h - 12h': 'Libre', '14h - 16h': 'Libre'}, 'Vendredi': {'8h - 10h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': ['niveau A1'], 'total_eleve': 5, 'donne_necessaire': 1}}, '10h - 12h': {'Allemand': {'Formations_name': 'Anglais', 'niveau': [], 'total_eleve': 1, 'donne_necessaire': 1}}, '14h - 16h': 'Libre'}, 'Samedi': {'8h - 10h': 'Libre', '10h - 12h': 'Libre', '14h - 16h': 'Libre'}}
{'Anglais': {'heure': '14h - 16h', 'jours': 'Samedi'}, 'Allemand': {'heure': '14h - 16h', 'jours': 'Samedi'}}