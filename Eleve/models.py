from django.db import models
# Create your models here.
class Formations(models.Model):
    Nom = models.CharField()
    duree = models.IntegerField()
    level_number = models.IntegerField()
    Ecolage = models.IntegerField()
    Type_Formations = models.CharField()
    cours_semaine = models.IntegerField()
    Droit = models.IntegerField(default=30000)


class Eleve_class(models.Model):
    Nom = models.CharField()
    Prenom = models.CharField()
    Droit = models.BooleanField(default=False)
    Dossier = models.BooleanField(default=False)
    Profile = models.ImageField(upload_to='static/profile', default='default.jpg')
    Status = models.BooleanField(default=True)
    Numero = models.CharField()
    date = models.DateTimeField(auto_now_add=True)
class Formations_eleve(models.Model):
    Formations = models.ForeignKey(Formations,on_delete=models.CASCADE)
    Niveau = models.CharField()
    Reste_mois = models.IntegerField()
    Eleve_choix = models.ForeignKey(Eleve_class,on_delete=models.CASCADE)


# le nombre de mois restant pour le l'eleve
class Mois_class(models.Model):
    Nom = models.CharField()
    Ecolage = models.BooleanField(default=False)
    Numero_fa = models.CharField()
    Eleve = models.ForeignKey(Eleve_class,on_delete=models.CASCADE)
    Ecolage_payer = models.FloatField(default=False)
    Niveau = models.CharField()
    Formations = models.ForeignKey(Formations,on_delete=models.CASCADE)

# heure disponible
class Disponibilite(models.Model):
    Heure = models.CharField()

class Emplois_du_temps(models.Model):
    Heure = models.ForeignKey(Disponibilite,on_delete=models.CASCADE)
    type_de_Formations = models.ForeignKey(Formations,on_delete=models.CASCADE)
    Jour_de_la_semaine = models.CharField()
    Eleve = models.ForeignKey(Eleve_class,on_delete=models.CASCADE)
    Niveau = models.CharField()
    cles_unique = models.CharField()
    Status = models.BooleanField(default=True)


class Niveau_Par_Formations(models.Model):
    FK_formations = models.ForeignKey(Formations,on_delete=models.CASCADE)
    Niveaux = models.CharField()