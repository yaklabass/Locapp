from django.urls import path
from . import views


urlpatterns = [
    path('', views.locataire_index, name=''),
    # path('', views.index, name=''),
    path('register', views.register, name='register'),
    path('login', views.my_login, name='login'),
    path('adm-index', views.adm_index, name='adm-index'),
    path('logout', views.logout, name='logout'),
    # path('my-admin', views.my_admin, name='my-admin'),
    # path('dashboard', views.dashboard, name='dashboard'),
    #-------INDEX'S-------
    path('index-1', views.index1, name='index-1'),
    path('index-2', views.index2, name='index-2'),
    path('index-3', views.index3, name='index-3'),
    path('index-0', views.index0, name='index-0'),
    path('gerant-index', views.gerant_index, name='gerant-index'),
    path('appartements-disponibles', views.locataire_index2, name='appartements-disponibles'),
    # ------GERANT-------
    path('all-gerant', views.all_gerant, name='all-gerant'),
    path('add-gerant', views.add_gerant, name='add-gerant'),
    path('edit-gerant/<int:pk>/', views.edit_gerant, name='edit-gerant'),
    path('delete-gerant/<int:pk>', views.delete_gerant, name="delete-gerant"),
    path('gerant-profile', views.gerant_profile, name='gerant-profile'),
    # ----LOCATAIRE-------
    path('all-locataire', views.all_locataire, name='all-locataire'),
    path('add-locataire', views.add_locataire, name='add-locataire'),
    path('edit-locataire/<int:pk>/', views.edit_locataire, name='edit-locataire'),
    path('delete-locataire/<int:pk>', views.delete_locataire, name="delete-locataire"),

    # ----Appartement-------
    path('all-appartement/', views.all_appartement, name='all-appartement'),
    path('add-appartement/', views.add_appartement, name='add-appartement'),
    path('edit-appartement/<int:pk>/', views.edit_appartement, name='edit-appartement'),
    path('delete-appartement/<int:pk>/', views.delete_appartement, name='delete-appartement'),
    path('all-gerant-appartement/', views.appartements_gerant, name='all-gerant-appartement'),
    path('detail-appartement/<int:appartement_id>/', views.detail_appartement, name='detail-appartement'),
    #-----APP PROFILE -------
    path('app-profile', views.app_profile, name='app-profile'),
    #-----Reservation----------
    path('all-reservatio/', views.all_reservation, name='all-reservation'),
    path('edit-reservation/<int:reservation_id>/', views.edit_reservation, name='edit-reservation'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete-reservation'),
    path('add-reservation/', views.add_reservation, name='add-reservation'),
    path('create-reservation/<int:appartement_id>/', views.create_reservation, name='create-reservation'),
    path('create-reservation-moi/<int:appartement_id>/', views.create_reservation_moi, name='create-reservation-moi'),
    path('reservation-success/<int:reservation_id>/', views.reservation_success, name='reservation-success'),
    path('reservation-moi-success/<int:reservation_id>/', views.reservation_moi_success, name='reservation-moi-success'),
    path('reservations-en-attente/', views.reservations_en_attente, name='reservations-en-attente'),
    path('edit-reservation-statut/<int:reservation_id>/', views.edit_statut_reservation, name='edit-reservation-statut'),
    path('edit-reservation-moi-statut/<int:reservation_id>/', views.edit_statut_reservation_moi, name='edit-reservation-moi-statut'),
    path('locataire-reservation/', views.locataire_reservation, name='locataire-reservation'),
    path('reservation-jour-confirme-detail/<int:reservation_id>/', views.reservation_jour_confirme_detail, name='reservation-jour-confirme-detail'),
    path('reservation-payee-detail/<int:reservation_id>/', views.reservation_payee_detail, name='reservation-payee-detail'),
    path('reservation-moi-confirme-detail/<int:reservation_id>/', views.reservation_moi_confirme_detail, name='reservation-moi-confirme-detail'),
    path('create-payement-bankili/<int:reservation_id>/', views.create_payement_bankili, name='create-payement-bankili'),
    path('create-payement-sedad/<int:reservation_id>/', views.create_payement_sedad, name='create-payement-sedad'),
    path('create-payement-bimbank/<int:reservation_id>/', views.create_payement_bimbank, name='create-payement-bimbank'),
    path('payement-success/', views.payement_success, name='payement-success'),
    path('paiements-en-cours/', views.paiements_en_cours, name='paiements-en-cours'),
    path('paiement/confirmer/<int:paiement_id>/', views.confirmer_paiement, name='confirmer-paiement'),
    path('paiement/refuser/<int:paiement_id>/', views.refuser_paiement, name='refuser-paiement'),
    path('a-propos-de-nous/', views.a_propos_de_nous, name='a-propos-de-nous'),
]


