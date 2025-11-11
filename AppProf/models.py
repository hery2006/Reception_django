from datetime import datetime
from django.db import models
from Eleve.models import Formations
from Main.models import *
# Create your models here.
class Prof_models(models.Model):
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Cin = models.CharField(max_length=20)
    Types_formation = models.ForeignKey('Eleve.Formations', on_delete=models.CASCADE)
    Duree = models.CharField(max_length=50)
    Date_embauche = models.DateField(default=datetime.now)
    Payement = models.FloatField()
    Status = models.BooleanField(default=True)
class Prof_Mois_payement(models.Model):
    Mois = models.CharField()
    Years_reference = models.ForeignKey(Annee_Class,on_delete=models.CASCADE)

class Prof_Paiement(models.Model):
    Prof_id = models.ForeignKey(Prof_models,on_delete=models.CASCADE)
    Mois= models.ForeignKey(Prof_Mois_payement,on_delete=models.CASCADE)
    years = models.ForeignKey(Annee_Class,on_delete=models.CASCADE)
    Work_day = models.FloatField(default=0)
    Seance_Hours = models.FloatField(default=0)
    Total_Salary_month = models.FloatField(default=0)
    Observations = models.CharField()
    Status = models.CharField(default=False)

