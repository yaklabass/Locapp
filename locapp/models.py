from django.db import models
from django.contrib.auth.models import User
from datetime import date 
from django.utils import timezone









# - Classe gerant

class Gerant(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    nomGER =  models.CharField(max_length=100)
    prenomGER =  models.CharField(max_length=100)
    telGER = models.CharField(max_length=8) 
    adresseGER = models.CharField(max_length=50)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
     
    def __str__(self):

            return self.nomGER 



    



# - Classe locateur
class Locataire(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    nomLOC =  models.CharField(max_length=100)
    prenomLOC =  models.CharField(max_length=100)
    telLOC = models.CharField(max_length=8)
    adresse = models.CharField(max_length=50)

    def __str__(self):

            return self.nomLOC 




# # - Classe appartement


class Appartement(models.Model):
    CATEGORIE_CHOICES = [
        ('jour', 'Par Jour'),
        ('mois', 'Par Mois'),
    ]
    nomAP =  models.CharField(max_length=100)
    telAP = models.CharField(max_length=8)
    adresseAP = models.CharField(max_length=50)
    nb_chambres = models.IntegerField()
    nb_salles_bains=models.IntegerField()
    description = models.CharField(max_length=2000)
    Gerant = models.ForeignKey(Gerant, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='appartements/', blank=True, null=True)
    image1 = models.ImageField(upload_to='appartements/', blank=True, null=True)
    image2 = models.ImageField(upload_to='appartements/', blank=True, null=True)
    image3 = models.ImageField(upload_to='appartements/', blank=True, null=True)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES)
    


    def __str__(self):

            return self.nomAP 
    

    






# - Classe reservation 

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Payée'),
        ('Pending', 'En attente'),
        ('Canceled', 'Annulée'),
        ('Success', 'Confirmée'),
    ]

    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    appartement = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    date_debut = models.DateField(default=date.today)
    date_fin = models.DateField(default=date.today)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES)
    frais = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Réservation {self.id} - {self.locataire.nomLOC} / {self.appartement.nomAP}"
    


class ReservationMoi(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'En attente'),
        ('Confirmed', 'Confirmée'),
        ('Canceled', 'Annulée'),
        ('Completed', 'Terminée'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Electronic', 'Électronique'),
    ]

    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    appartement = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    date_debut = models.DateField(default=date.today)
    jour_payement = models.IntegerField()  # Day of the month for payment
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    frais = models.DecimalField(max_digits=10, decimal_places=2)
    methode_payement = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    signature_locataire = models.ImageField(upload_to='signatures/', blank=True, null=True)
    signature_gerant = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return f"Réservation Moi {self.id} - {self.locataire.nomLOC} / {self.appartement.nomAP}"
# - Classe Paiement 

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('confirme', 'Confirmé'),
        ('refuse', 'Refusé'),
    ]

    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, blank=True, null=True)
    numero_telephone = models.CharField(max_length=15, blank=True, null=True)
    numero_de_transfert = models.CharField(max_length=50, blank=True, null=True)
    capture_ecran = models.ImageField(upload_to='payement_captures/', blank=True, null=True)
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='en_cours',
    )


    def __str__(self):
        return f"Paiement {self.id} pour Réservation {self.reservation.id}"


    

   
   

# # #     # def __str__(self):

# # #     #     return self.first_name + ' ' + self.last_name





















# class Utilisateur(AbstractUser):
#     GERANT = 'gerant'
#     CLIENT = 'client'
#     ROLE_CHOICES = [
#         (GERANT, 'Gérant'),
#         (CLIENT, 'Client'),
#     ]

#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=GERANT)
#     # Ajoutez des champs personnalisés ou des méthodes au besoin
    
#     # Définissez les relations avec les groupes et les permissions directement dans la classe du modèle
#     groups = models.ManyToManyField('auth.Group', related_name='groupes_utilisateur', blank=True)
#     user_permissions = models.ManyToManyField('auth.Permission', related_name='permissions_utilisateur', blank=True)

#     class Meta:
#         # Spécifiez le nom de la table pour éviter les problèmes de migration
#         db_table = 'utilisateur'



class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('gerant', 'Gerant'),
        ('locataire', 'Locataire'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    def __str__(self):
        return self.user.username