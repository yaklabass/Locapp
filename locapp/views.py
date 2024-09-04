from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
# from matplotlib.pyplot import plot
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth  #logout
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from datetime import date
import pandas as pd
import plotly.express as px
import numpy as np
from django.db.models import Sum
import plotly.graph_objects as go
from plotly.offline import plot





# --------LES INDEX'S--------------


# - index 
@login_required(login_url='login')
def index(request):
    return render(request,'locapp/index.html')





# - index gerant
@login_required(login_url='login')
def gerant_index(request):
    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Récupérer l'objet Gerant correspondant
    gerant = Gerant.objects.get(user=user)

    # Récupérer le total des appartements du gérant connecté
    total_appartements = Appartement.objects.filter(Gerant=gerant).count()

    # Récupérer le total des réservations
    total_reservations = Reservation.objects.filter(appartement__Gerant=gerant).count()

    # Récupérer le total des revenus
    total_revenue = Reservation.objects.filter(appartement__Gerant=gerant).aggregate(Sum('frais'))['frais__sum'] or 0

    # Calculer le taux d'occupation
    today = date.today()
    total_reservations_actives = Reservation.objects.filter(
        appartement__Gerant=gerant,
        date_debut__lte=today,
        date_fin__gte=today
    ).exclude(statut__in=['Canceled', 'Pending']).count()
    occupation_rate = (total_reservations_actives / total_appartements) * 100 if total_appartements > 0 else 0
    occupation_rate = round(occupation_rate, 2)  # Arrondir à deux chiffres après la virgule

    # Récupérer le total des réservations annulées
    total_reservations_annulees = Reservation.objects.filter(appartement__Gerant=gerant, statut='Canceled').count()

    # Calculer le taux d'annulation
    taux_annulation = (total_reservations_annulees / total_reservations) * 100 if total_reservations > 0 else 0
    taux_annulation = round(taux_annulation, 2)  # Arrondir à deux chiffres après la virgule

    context = {
        'total_appartements': total_appartements,
        'total_reservations': total_reservations,
        'total_revenue': total_revenue,
        'occupation_rate': occupation_rate,
        'total_reservations_annulees': total_reservations_annulees,
        'taux_annulation': taux_annulation
    }
    return render(request, 'gerant/index.html', context)



# - index admin
@login_required(login_url='login')
def adm_index(request):
    appartements = Appartement.objects.all()
    reservations = Reservation.objects.filter(statut='Confirmée')
    total_gerant = Gerant.objects.count()
    total_locataire = Locataire.objects.count()
    total_appartements = appartements.count()
    total_reservations = Reservation.objects.count()
    total_revenue = reservations.aggregate(Sum('frais'))['frais__sum'] or 0

    if total_appartements > 0:
        occupation_rate = (total_reservations / total_appartements) * 100
        occupation_rate = round(occupation_rate, 2)  # Garder seulement deux chiffres après la virgule
    else:
        occupation_rate = 0

    # Vérifiez les valeurs récupérées
    reservations_values = list(reservations.values('date_debut', 'frais'))
    print(reservations_values)  # Affichez les valeurs pour débogage

    if reservations_values:  # Assurez-vous qu'il y a des données avant de créer le DataFrame
        reservations_df = pd.DataFrame(reservations_values)
        
        # Vérifiez que 'date_debut' est bien dans le DataFrame
        if 'date_debut' in reservations_df.columns:
            reservations_df['date_debut'] = pd.to_datetime(reservations_df['date_debut'])
            reservations_df['month'] = reservations_df['date_debut'].dt.to_period('M')
            reservations_per_month = reservations_df.groupby('month').size().reset_index(name='reservations')
            revenue_per_month = reservations_df.groupby('month')['frais'].sum().reset_index(name='revenue')

            reservations_per_month_fig = px.line(reservations_per_month, x='month', y='reservations', title='Réservations par mois')
            revenue_per_month_fig = px.line(revenue_per_month, x='month', y='revenue', title='Revenus par mois')

            reservations_per_month_graph = reservations_per_month_fig.to_html(full_html=False, default_height=500, default_width=700)
            revenue_per_month_graph = revenue_per_month_fig.to_html(full_html=False, default_height=500, default_width=700)

            # Top 5 des appartements les plus réservés
            if 'appartement' in reservations_df.columns:
                top_appartements = reservations_df['appartement'].value_counts().nlargest(5).reset_index(name='reservations')
                top_appartements_fig = px.bar(top_appartements, x='index', y='reservations', title='Top 5 des appartements les plus réservés')
                top_appartements_graph = top_appartements_fig.to_html(full_html=False, default_height=500, default_width=700)
            else:
                top_appartements_graph = None
        else:
            reservations_per_month_graph = None
            revenue_per_month_graph = None
            top_appartements_graph = None
    else:
        reservations_per_month_graph = None
        revenue_per_month_graph = None
        top_appartements_graph = None

    labels = ["ISCAE","FST","IUP","ESP","FSJE"]
    values = [70,150,20,12,90]

    bar_color = 'green'  # Specify the color of the bars

    fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker=dict(color=bar_color, line=dict(color='white', width=1.5)),  # Apply color and border to the bars
            opacity=0.8,  # Set the opacity of the bars
            textposition='auto'  # Set the position of the value labels
        )])

    fig.update_layout(
            title='Les reservations par 5 top appartements',
            xaxis=dict(
                title='Appartements',
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title='Nombre',
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            plot_bgcolor='white',
            font=dict(
                family='Arial',
                color='black',
                size=12
            ),
            width=500,  # Set the width of the graph
            height=400  # Set the height of the graph
        )
        
    plot_div = plot(fig, output_type='div')


    # Labels and values
    labels = ["Raha", "Free zone", "Nouzha", "Vasq", "Azalai"]
    values = [70, 150, 20, 12, 90]

    # Pie chart color scheme
    colors = ['green', 'blue', 'orange', 'red', 'purple']

    # Create the figure
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=1.5)),  # Apply colors and border to the slices
        opacity=0.8,  # Set the opacity of the slices
        textinfo='label+percent',  # Show label and percent on the slices
        insidetextorientation='radial'  # Text orientation
        )])

    # Update layout
    fig.update_layout(
        title='Les reservations par 5 top appartements',
        plot_bgcolor='white',
        font=dict(
            family='Arial',
            color='black',
            size=12
        ),
        width=500,  # Set the width of the graph
        height=400  # Set the height of the graph
    )

    # Generate the HTML div
    plot_divs = plot(fig, output_type='div')


    context = {
        'total_appartements': total_appartements,
        'total_reservations': total_reservations,
        'total_revenue': total_revenue,
        'occupation_rate': occupation_rate,
        'reservations_per_month_graph': reservations_per_month_graph,
        'revenue_per_month_graph': revenue_per_month_graph,
        'top_appartements_graph': top_appartements_graph,
        'total_gerant': total_gerant,
        'total_locataire': total_locataire,
        'plot_divs' : plot_divs,

    }

    return render(request, 'adm/index.html', context)


    # total_gerant = Gerant.objects.count()
    # total_locataire = Locataire.objects.count()
    # total_appartement = Appartement.objects.count()
    # reservations = Reservation.objects.all()

    # context = {
    #     'total_gerant': total_gerant,
    #     'total_locataire': total_locataire,
    #     'total_appartement': total_appartement,
    #     'reservations': reservations,
    # }
    # return render(request,'adm/index.html',context)









# - index locataire
def locataire_index(request):
    
    appartements_jour = Appartement.objects.filter(categorie='Jour')
    appartements_mois = Appartement.objects.filter(categorie='Mois')
    return render(request, 'locataire/index.html', {
        'appartements_jour': appartements_jour,
        'appartements_mois': appartements_mois
    })


def locataire_index2(request):
    today = date.today()
    reserved_appartements_ids = Reservation.objects.filter(
        date_debut__lte=today, date_fin__gte=today
    ).exclude(statut__in=['Canceled', 'Pending']).values_list('appartement_id', flat=True)
    
    available_appartements = Appartement.objects.exclude(id__in=reserved_appartements_ids)
    return render(request, 'locataire/index.html', {'appartements': available_appartements})





# - index 0
def index0(request):
    return render(request,'locapp/index-0.html')






# - index 1
@login_required(login_url='login')
def index1(request):
    return render(request,'locapp/index-1.html')




# - index 2
@login_required(login_url='login')
def index2(request):
    return render(request,'locapp/index-2.html')



# - index 3
@login_required(login_url='login')
def index3(request):
    return render(request,'locapp/index-3.html')






# -----APP PROFILE -----------

@login_required(login_url='login')
def app_profile(request):
    return render(request,'app-profile.html')





# -------GERANT--------



# - Tous les gerants
@login_required(login_url='login')
def all_gerant(request):

    my_gerants = Gerant.objects.all()

    context = {'gerants': my_gerants}

    return render(request, 'adm/all-gerant.html', context=context)





# - ajouter un gerant
@login_required(login_url='login')
def add_gerant(request):
    form = addGerantForm()

    if request.method == "POST":
        form = addGerantForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            # Créer profil Gerant
            Gerant.objects.create(
                user=user,
                nomGER=form.cleaned_data.get("first_name"),
                prenomGER=form.cleaned_data.get("last_name"),
                adresseGER=form.cleaned_data.get("adresse"),
                telGER=form.cleaned_data.get("telephone")
            )
            Profile.objects.create(
                user=user,
                role='gerant'
            )

            messages.success(request, "Votre gérant a été créé!")
            return redirect("all-gerant")

    context = {'form': form}
    return render(request, 'adm/add-gerant.html', context=context)

        
        



# - modifier un gerant
@login_required(login_url='login')
def edit_gerant(request, pk):

    gerant = get_object_or_404(Gerant, pk=pk)
    user = gerant.user
    
    if request.method == 'POST':
        form = editGerantForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            gerant.nomGER = form.cleaned_data.get("first_name")
            gerant.prenomGER = form.cleaned_data.get("last_name")
            gerant.adresseGER = form.cleaned_data.get("adresse")
            gerant.telGER = form.cleaned_data.get("telephone")
            gerant.save()
            messages.success(request, "Votre gerant a été modifié avec succès!")
            return redirect("all-locataire")
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier les informations fournies.")
    
    else:
        initial_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'adresse': gerant.adresseGER,
            'date_joined': user.date_joined,
            'telephone': gerant.telGER,
            'email': user.email
        }
        form = editGerantForm(instance=user, initial=initial_data)
    
    context = {'form': form}
    return render(request, 'adm/edit-gerant.html', context=context)






# -profil du gerant
@login_required(login_url='login')
def gerant_profile(request):
    return render(request,'adm/profile-gerant.html')



# -----LOCATAIRE--------



# - Tous les locataire
@login_required(login_url='login')
def all_locataire(request):

    my_locataires = Locataire.objects.all()

    context = {'locataires':  my_locataires}

    return render(request, 'adm/all-locataire.html', context=context)
    



# - ajouter un locataire
@login_required(login_url='login')
def add_locataire(request):


    form = addLocataireForm()

    if request.method == "POST":

              form = addLocataireForm(request.POST)

              if form.is_valid():

                form.save()

                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)


                # creer profle Locataire

                Locataire.objects.create(
                user = user,
                nomLOC = form.cleaned_data.get("first_name"),
                prenomLOC = form.cleaned_data.get("last_name"),
                adresse = form.cleaned_data.get("adresse"),
                telLOC = form.cleaned_data.get("telephone")
                )
                Profile.objects.create(
                user=user,
                role='locataire'
                )

                messages.success(request, "Votre locataire a ete creer!")

                return redirect("all-locataire")

    context = {'form': form}

            
    return render(request, 'adm/add-locataire.html', context=context)
   



# - modifier un locataire
@login_required(login_url='login')

def edit_locataire(request, pk):
    locataire = get_object_or_404(Locataire, pk=pk)
    user = locataire.user
    
    if request.method == 'POST':
        form = editLocataireForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            locataire.nomLOC = form.cleaned_data.get("first_name")
            locataire.prenomLOC = form.cleaned_data.get("last_name")
            locataire.adresse = form.cleaned_data.get("adresse")
            locataire.telLOC = form.cleaned_data.get("telephone")
            locataire.save()
            messages.success(request, "Votre locataire a été modifié avec succès!")
            return redirect("all-locataire")
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier les informations fournies.")
    
    else:
        initial_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'adresse': locataire.adresse,
            'date_joined': user.date_joined,
            'telephone': locataire.telLOC,
            'email': user.email
        }
        form = editLocataireForm(instance=user, initial=initial_data)
    
    context = {'form': form}
    return render(request, 'adm/edit-locataire.html', context)



# -----APPARTEMENT--------



# - Tous les appartements
@login_required(login_url='login')
def all_appartement(request):
    appartements = Appartement.objects.all()
    context = {
        'appartements': appartements
    }
    return render(request, 'adm/all-appartement.html', context)


def detail_appartement(request, appartement_id):
    appartement = get_object_or_404(Appartement, pk=appartement_id)
    return render(request, 'locataire/detail-appart.html', {'appartement': appartement})

# - Tous les appartements d'un gérant
@login_required(login_url='login')
def appartements_gerant(request):
    # Récupère le gérant associé à l'utilisateur connecté
    gerant = get_object_or_404(Gerant, user=request.user)
    # Récupère les appartements gérés par ce gérant
    appartements = Appartement.objects.filter(Gerant=gerant)

    context = {
        'appartements': appartements
    }
    return render(request, 'gerant/all-gerant-appartement.html', context)



# - ajouter un appartement
@login_required(login_url='login')
def add_appartement(request):
    if request.method == "POST":
        form = addAppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre appartement a été créé avec succès!")
            return redirect("all-appartement")
    else:
        form = addAppForm()
    context = {'form': form}
    return render(request, 'adm/add-appartement.html', context)



# - modifier un appartement
@login_required(login_url='login')
def edit_appartement(request, pk):
    appartement = get_object_or_404(Appartement, pk=pk)
    if request.method == 'POST':
        form = addAppForm(request.POST, request.FILES, instance=appartement)
        if form.is_valid():
            form.save()
            messages.success(request, "L'appartement a été modifié avec succès!")
            return redirect('all-appartement')
    else:
        form = addAppForm(instance=appartement)
    context = {'form': form}
    return render(request, 'adm/edit-appartement.html', context)




#---RESERVATION-----

# - Tous les reservations
@login_required(login_url='login')
def all_reservation(request):
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    return render(request, 'adm/all-reservation.html', context)

#add reservation
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm-index')  # Redirigez vers la liste des réservations ou une autre vue appropriée
    else:
        form = ReservationForm()
    
    return render(request, 'adm/add-reservation.html', {'form': form})




#edit_reseve

def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('adm-index')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'adm/edit-reservation.html', {'form': form})


#Res APP

@login_required(login_url='login')
def create_res(request):
    return render(request,'locataire/create-reservation.html')



# création de reservation à partir de locataire

@login_required
def create_reservation(request, appartement_id):
    appartement = get_object_or_404(Appartement, id=appartement_id)
    locataire = get_object_or_404(Locataire, user=request.user)
    if request.method == 'POST':
        form = ReservationForm2(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.locataire = locataire  # Assigner l'objet Locataire
            reservation.appartement = appartement
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']
            delta = (date_fin - date_debut).days
            reservation.frais = delta * appartement.prix
            reservation.statut = 'Pending'
            reservation.save()
            return redirect('reservation-success',reservation_id=reservation.pk)
    else:
        form = ReservationForm2()
    return render(request, 'locataire/create-reservation.html', {'form': form, 'appartement': appartement})

def create_reservation_moi(request, appartement_id):
    locataire = get_object_or_404(Locataire, user=request.user)
    appartement = get_object_or_404(Appartement, pk=appartement_id)
    if request.method == "POST":
        form = ReservationMoisForm(request.POST, request.FILES)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.locataire = locataire
            reservation.appartement = appartement
            reservation.frais = appartement.prix
            reservation.statut = 'Pending'
            reservation.save()
            return redirect('reservation-moi-success', reservation_id=reservation.id)
    else:
        form = ReservationMoisForm()
    return render(request, 'locataire/create-reservation-moi.html', {'form': form, 'appartement': appartement})


@login_required
def reservation_success(request,reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'locataire/reservation-success.html', {'reservation': reservation})

@login_required
def reservation_moi_success(request, reservation_id):
    reservation_moi = get_object_or_404(ReservationMoi, pk=reservation_id)
    conditions = [
        "L'eau et l'électricité seront payées par le locataire.",
        "Le locataire est responsable des petites réparations et de l'entretien courant de l'appartement.",
        "L'appartement doit être utilisé uniquement à des fins résidentielles."
    ]
    return render(request, 'locataire/reservation-moi-success.html', {
        'reservation': reservation_moi,
        'conditions': conditions
    })



# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# LOGIN


def my_login(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('adm-index')
                else:
                    try:
                        profile = Profile.objects.get(user=user)
                        if profile.role == 'gerant':
                            return redirect('gerant-index')
                        elif profile.role == 'locataire':
                            return redirect('')
                    except Profile.DoesNotExist:
                        msg = 'User profile does not exist.'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "locapp/login.html", {"form": form, "msg": msg})


# REGISTER

def register(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            # Créer profil Locataire
            Locataire.objects.create(
                user=user,
                nomLOC=form.cleaned_data.get("username"),
                adresse=form.cleaned_data.get("adresse"),
                telLOC=form.cleaned_data.get("telephone")
            )
            Profile.objects.create(
                user=user,
                role='locataire'
            )

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "locapp/register.html", {"form": form, "msg": msg, "success": success})


# # - dashboard
# @login_required(login_url='login')
# def dashboard(request):

#     # my_records = Record.objects.all()

#     # context = {'records': my_records}

#     return render(request,'locapp/dashboard.html')


# - User Logout

def     logout(request):

    auth.logout(request)

    return redirect("login")



#-----DELETE LOCATAIRE-------

@login_required(login_url='my-login')
def delete_locataire(request, pk):

    locataire = Locataire.objects.get(pk=pk)

    locataire.delete()

    messages.success(request, "Ton locataire a ete supprimé!")

    return redirect("all-locataire")



#-----DELETE GERANT-------

@login_required(login_url='my-login')
def delete_gerant(request, pk):

    gerant = Gerant.objects.get(pk=pk)

    gerant.delete()

    messages.success(request, "Ton locataire a ete supprimé!")

    return redirect("all-gerant")


#-----DELETE APPARTEMENT-------

@login_required(login_url='login')
def delete_appartement(request, pk):
    appartement = get_object_or_404(Appartement, pk=pk)
  
    appartement.delete()

    messages.success(request, "L'appartement a été supprimé avec succès!")
    return redirect('all-appartement')
   

#Supprimer-reserve

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('adm-index')  # Redirigez vers le tableau de bord ou une autre page appropriée



@login_required
def notification(request):
    if request.user.groups.filter(name='Gerant').exists():
        gerant = Gerant.objects.get(user=request.user)
        pending_reservations_count = Reservation.objects.filter(appartement__Gerant=gerant, statut='Pending').count()
    else:
        pending_reservations_count = 0

    context = {
        'pending_reservations_count': pending_reservations_count,
        # other context data
    }
    return render(request, 'gerant/navheader.html', context)

# def is_manager(user):
#     return user.groups.filter(name='Gerant').exists()

# @user_passes_test(is_manager)
@login_required
def reservations_en_attente(request):
    gerant = get_object_or_404(Gerant, user=request.user)
    reservations = Reservation.objects.filter(appartement__Gerant=gerant, statut='Pending')
    reservations_moi = ReservationMoi.objects.filter(appartement__Gerant=gerant, statut='Pending')
    return render(request, 'gerant/reservations-en-attente.html', {
        'reservations': reservations,
        'reservations_moi': reservations_moi
    })



def edit_statut_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == "POST":
        form = ReservationStatusForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('gerant-index')
    else:
        form = ReservationStatusForm(instance=reservation)
    return render(request, 'gerant/edit-reservation-statut.html', {'form': form})


def edit_statut_reservation_moi(request, reservation_id):
    reservation = get_object_or_404(ReservationMoi, pk=reservation_id)
    if request.method == "POST":
        form = ReservationMoiStatusForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('gerant-index')
    else:
        form = ReservationMoiStatusForm(instance=reservation)
    return render(request, 'gerant/edit-reservation-statut.html', {'form': form})

@login_required
def locataire_reservation(request):
    locataire = get_object_or_404(Locataire, user=request.user)
    reservations = Reservation.objects.filter(locataire=locataire, statut__in=['Confirmed', 'Success','Paid','Pending'])
    reservations_moi = ReservationMoi.objects.filter(locataire=locataire, statut__in=['Confirmed', 'Canceled'])
    return render(request, 'locataire/locataire-reservation.html', {
        'reservations': reservations,
        'reservations_moi': reservations_moi,
    })

@login_required
def reservation_jour_confirme_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, locataire__user=request.user)
    return render(request, 'locataire/reservation-jour-confirme-detail.html', {'reservation': reservation})

@login_required
def reservation_payee_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'locataire/reservation-payee-detail.html', {'reservation': reservation})

@login_required
def reservation_moi_confirme_detail(request, reservation_id):
    reservation = get_object_or_404(ReservationMoi, id=reservation_id)
    appartement = reservation.appartement
    gerant = appartement.Gerant
    conditions = [
        "L'eau et l'électricité seront payées par le locataire.",
        "Le locataire est responsable des petites réparations et de l'entretien courant de l'appartement.",
        "L'appartement doit être utilisé uniquement à des fins résidentielles."
    ]
    return render(request, 'locataire/reservation-moi-confirm-detail.html', {
        'reservation': reservation,
        'gerant': gerant,
        'conditions': conditions
    })


@login_required
def create_payement_bankili(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    appartement = reservation.appartement

    if request.method == 'POST':
        form = PayementForm(request.POST, request.FILES)
        if form.is_valid():
            payement = form.save(commit=False)
            payement.reservation = reservation
            payement.save()
            return redirect('payement-success')
    else:
        form = PayementForm()

    return render(request, 'locataire/create-payement-bankili.html', {
        'form': form,
        'appartement': appartement
    })

login_required
def create_payement_sedad(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    appartement = reservation.appartement

    if request.method == 'POST':
        form = PayementForm(request.POST, request.FILES)
        if form.is_valid():
            payement = form.save(commit=False)
            payement.reservation = reservation
            payement.save()
            return redirect('payement-success')
    else:
        form = PayementForm()

    return render(request, 'locataire/create-payement-sedad.html', {
        'form': form,
        'appartement': appartement
    })

login_required
def create_payement_bimbank(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    appartement = reservation.appartement

    if request.method == 'POST':
        form = PayementForm(request.POST, request.FILES)
        if form.is_valid():
            payement = form.save(commit=False)
            payement.reservation = reservation
            payement.save()
            return redirect('payement-success')
    else:
        form = PayementForm()

    return render(request, 'locataire/create-payement-bimbank.html', {
        'form': form,
        'appartement': appartement
    })

@login_required
def payement_success(request):
    return render(request, 'locataire/payement-success.html')


@login_required
def paiements_en_cours(request):
    gerant = get_object_or_404(Gerant, user=request.user)
    paiements = Paiement.objects.filter(reservation__appartement__Gerant=gerant, statut='en_cours')
    return render(request, 'gerant/paiements-en-cours.html', {'paiements': paiements})


@login_required
def confirmer_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    reservation = paiement.reservation
    paiement.statut = 'confirme'
    paiement.save()
    reservation.statut = 'Paid'
    reservation.save()
    return redirect('gerant-index')

@login_required
def refuser_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    paiement.statut = 'refuse'
    paiement.save()
    return redirect('paiements-en-cours')



@login_required
def a_propos_de_nous(request):
    return render(request, 'locataire/a-propos-de-nous.html')