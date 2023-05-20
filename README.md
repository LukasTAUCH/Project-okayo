# Project-okayo

Voici le fichier sujet.sql qui permet de décrire le modèle de données relationnel qui serait lié à la gestion
de cette fonctionnalité.

Ensuite le fichier peuplement.sql qui permet de remplir les différentes tables suivant l'exemple donné par le sujet.
Ainsi que 2 fonctions pour remplir automatiquement les lignes de facture et les factures des clients

Le fichier api.py est un code permettant de créer une instance Flask avec le code RESTAPI (update,create,get,delete) les tables clients, produits et taux tva.
Le code python est lancé en local avec la commande : python api.py

* Serving Flask app 'api'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 389-932-572

Grace à l'application "Insomnia" nous pouvons utiliser les différentes fonctions qui permettent de modifier la base de donnée avec du "json".
