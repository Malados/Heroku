# Generated by Django 3.1.7 on 2021-04-08 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('prenom', models.CharField(max_length=200, null=True)),
                ('categorie', models.CharField(blank=True, choices=[('CADRE', 'Cadre'), ('OUVRIER', 'Ouvrier'), ('AGRICULTEUR', 'Agriculteur'), ('ARTISAN', 'Artisan'), ('EMPLOYE', 'Employe'), ('RETRAITE', 'Retraite'), ('AUTRE', 'Autre')], max_length=200)),
                ('date_naissance', models.DateField(null=True)),
                ('numero_telephone', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('genre', models.CharField(blank=True, choices=[('CLIENT', 'Client'), ('CLIENT_VALIDE', 'Client Valide'), ('CLIENT_INTERDIT', 'Client Interdit')], max_length=100)),
                ('client', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('payee', models.BooleanField(default=False)),
                ('envoyee', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.client')),
            ],
        ),
        migrations.CreateModel(
            name='Marchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=7)),
                ('genre', models.CharField(blank=True, choices=[('DECORATION', 'Decoration'), ('EXTERIEUR', 'Exterieur'), ('MEUBLE', 'Meuble')], max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Routage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('type_envoie', models.CharField(blank=True, choices=[('MAIL', 'Mail'), ('PAPIER_ECONOMIQUE', 'Papier Economique'), ('PAPIER_STANDARD', 'Papier Standard'), ('PAPIER_SUPERIEUR', 'Papier Superieur')], max_length=200)),
                ('liste_client', models.FileField(blank=True, null=True, upload_to='')),
                ('liste_marchandise', models.FileField(blank=True, null=True, upload_to='')),
                ('valid??e', models.BooleanField(default=False)),
                ('envoy??e', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ListeMarchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(blank=True, default=0, null=True)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('trait??', models.BooleanField(default=False)),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.commande')),
                ('marchandise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.marchandise')),
            ],
        ),
        migrations.CreateModel(
            name='AdresseLivraison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=200)),
                ('ville', models.CharField(max_length=200)),
                ('pays', models.CharField(max_length=200)),
                ('code_postale', models.CharField(max_length=200)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.client')),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.commande')),
            ],
        ),
    ]
