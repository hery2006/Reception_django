from django.contrib import admin
from .models import *
# Register your models here.
class Formations_admin(admin.ModelAdmin):
    list_display = ('Nom','duree','level_number','Ecolage',"Type_Formations",'cours_semaine')
    list_filter = ('Nom',)
    search_fields = ('Nom','duree')

class Eleve_admin(admin.ModelAdmin):
    list_display=('Nom','Prenom','Droit','Dossier','Profile')
    search_fields=('Nom','Prenom','Dossier')

class emplois_admin(admin.ModelAdmin):
    list_display=('Heure','type_de_Formations','Jour_de_la_semaine','Eleve')

class Disponibilite_admin(admin.ModelAdmin):
    list_display = ('Heure',)

admin.site.register(Formations,Formations_admin)
admin.site.register(Eleve_class,Eleve_admin)
admin.site.register(Emplois_du_temps,emplois_admin)
admin.site.register(Disponibilite,Disponibilite_admin)