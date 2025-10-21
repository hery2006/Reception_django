liste = list(set([None if x == 8 or x == 2 or x == 5 else x for x in range(12)]))

def Pop_None(liste):
    for num,valeur in enumerate(liste):
        if valeur == None:
            liste.pop(num)
    return liste

print(Pop_None(liste=liste))