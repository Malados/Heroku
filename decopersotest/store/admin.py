from django.contrib import admin
from django.core import serializers
from .models import *
import requests
import xml.etree.ElementTree as ET
import getpass
from xml.dom import minidom
import os
from django.conf import settings
from django.http import HttpResponse, Http404


def liste_routage(modeladmin, request, queryset):
    root = ET.Element("Root")
    Clients = ET.SubElement(root, 'Clients')
 
    for item in queryset:
        for adr in AdresseLivraison.objects.all():
            if adr.client_id == item.client_id:
                ET.SubElement(Clients, 'client', nom = item.nom, prenom= item.prenom, email=item.email, adresse = adr.adresse, ville = adr.ville, codepostale = adr.code_postale)

    data = ET.ElementTree(root)
    save_path_file = "static/routage/routageclient.xml"
    data.write(save_path_file, encoding='UTF-8', xml_declaration = True)

    response = HttpResponse(
        open("static/routage/routageclient.xml", 'rb').read())
    response['Content-Type'] = 'text/xml'
    response['Content-Disposition'] = 'attachment; filename= routageclient.xml'
    return response


def produit_routage(modeladmin, request, queryset):
    root = ET.Element("Root")
    Marchandises = ET.SubElement(root, 'Marchandises')

    for item in queryset:
        ET.SubElement(Marchandises, 'marchandise', nom = item.nom, prix = str(item.prix))

    data = ET.ElementTree(root)
    save_path_file = "static/routage/routagemarchandise.xml"
    data.write(save_path_file, encoding='UTF-8', xml_declaration = True)

    response = HttpResponse(
        open("static/routage/routagemarchandise.xml", 'rb').read())
    response['Content-Type'] = 'text/xml'
    response['Content-Disposition'] = 'attachment; filename= routagemarchandise.xml'
    return response


def liste_a_envoyer(modeladmin, request, queryset):
    print (queryset[0].liste_client)
    root = ET.Element("Root")
    Titre = ET.SubElement(root, 'Titre', type = queryset[0].nom)
    Description = ET.SubElement(root, 'Description').text =  queryset[0].description
    TypePapier = ET.SubElement(root, 'Typepapier', type = queryset[0].type_envoie)

    Marchandise = ET.parse(queryset[0].liste_marchandise)
    Client = ET.parse(queryset[0].liste_client)

    mar = Marchandise.find("./")
    cli = Client.find("./")

    root.append(mar)
    root.append(cli)

    data = ET.ElementTree(root)
    save_path_file = "static/routage/routageenvoie.xml"
    data.write(save_path_file, encoding='UTF-8', xml_declaration = True)

    response = HttpResponse(
        open("static/routage/routageenvoie.xml", 'rb').read())
    response['Content-Type'] = 'text/xml'
    response['Content-Disposition'] = 'attachment; filename= routageenvoie.xml'
    return response



@admin.register(Routage)
class RoutageAdmin(admin.ModelAdmin):
    # Fields
    fields = ('nom', 'description', 'type_envoie', 'liste_client',
              'liste_marchandise', 'validée', 'envoyée')

    # Barre de recherche
    search_fields = ('nom',)

    # List Display
    list_display = ('nom', 'description', 'validée', 'envoyée')

    # List_filter
    list_filter = ('validée', 'envoyée')
    # ordering
    ordering = ('nom',)
    actions = [liste_a_envoyer]


@admin.register(Marchandise)
class MarchandiseAdmin(admin.ModelAdmin):
    # Fields
    fields = ('nom', 'prix', 'genre', 'image')

    # Barre de recherche
    search_fields = ('nom',)

    # List Display
    list_display = ('nom', 'prix', 'genre')

    # List_filter
    list_filter = ('genre',)

    # ordering
    ordering = ('nom',)
    actions = [produit_routage]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Fields
    fields = ('client', 'nom', 'prenom', 'categorie',
              'date_naissance', 'numero_telephone', 'email', 'genre')

    # Barre de recherche
    search_fields = ('nom', )

    # List Display
    list_display = ('nom', 'genre', 'categorie')

    # List_filter
    list_filter = ('genre', 'categorie')

    # ordering
    ordering = ('nom',)

    actions = [liste_routage]


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    # Fields
    fields = ('client', 'complete', 'payee', 'envoyee', 'transaction_id')

    # Barre de recherche
    search_fields = ('client', 'transaction_id')

    # List Display
    list_display = ('client', 'date_commande', 'payee', 'envoyee')

    # List_filter
    list_filter = ('payee', 'envoyee')

    # ordering
    ordering = ('transaction_id',)


@admin.register(ListeMarchandise)
class ListeMarchandiseAdmin(admin.ModelAdmin):
    # Fields
    fields = ('commande', 'marchandise', 'quantite', 'traité')

    # Barre de recherche
    search_fields = ('commande', 'marchandise')

    # List Display
    list_display = ('commande', 'marchandise', 'quantite', 'traité')

    # List_filter
    list_filter = ('traité',)

    # ordering
    ordering = ('commande',)


@admin.register(AdresseLivraison)
class AdresseLivraisonAdmin(admin.ModelAdmin):
    # Fields
    fields = ('client', 'commande', 'adresse', 'ville', 'pays', 'code_postale')

    # Barre de recherche
    search_fields = ('client', 'commande')

    # List Display
    list_display = ('client', 'commande')

    # List_filter
    list_filter = ('ville',)

    # ordering
    ordering = ('client',)
