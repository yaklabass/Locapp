from django.contrib import admin

from locapp.models import *

# Register your models here.



admin.site.register(Appartement)
admin.site.register(Gerant)
admin.site.register(Locataire)
admin.site.register(Reservation)
admin.site.register(Paiement)
# admin.site.register(Utilisateur)