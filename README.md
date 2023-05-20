# Project-okayo

## sujet.sql
Voici le fichier sujet.sql qui permet de décrire le modèle de données relationnel qui serait lié à la gestion
de cette fonctionnalité.

### Conditions
Avec cette base de donnée, nous respectons les 3 conditions :

- Le total TTC d'une facture reste constant, même si les prix du catalogue changent :

chaque ligne de la facture, stockée dans la table Lignes_Facture, conserve le prix unitaire HT du produit et le taux de TVA au moment de la création de la facture. 
Ainsi, même si le prix du produit ou le taux de TVA change dans le catalogue, le total TTC de la facture ne change pas car il est calculé à partir des données de la table Lignes_Facture et non directement du catalogue.

- Les noms et les prix des produits peuvent évoluer dans le catalogue, mais restent inchangés sur les factures existantes :

Le prix unitaire HT est stocké dans la table Lignes_Facture au moment de la création de la facture. 
Donc, même si le prix d'un produit change dans le catalogue (table Produits), il reste inchangé sur toutes les factures existantes. 
Le nom du produit n'est pas stocké dans la Lignes_Facture, donc si vous voulez garder le nom du produit inchangé sur la facture, il faudra l'ajouter à la table Lignes_Facture.

- Le taux de TVA peut changer avec le temps et peut être différent pour chaque produit du catalogue :

Chaque produit dispose de son taux de TVA qui est stocké dans la table Taux_TVA. 
Si le taux de TVA doit changer pour un produit, un nouvel enregistrement doit être créé dans cette table avec la nouvelle valeur du taux de TVA et la date de début de validité. 
Au moment de la création d'une facture, le système peut choisir le taux de TVA approprié pour chaque produit en fonction de la date de la facture. 
Cependant, une fois la facture créée, le taux de TVA utilisé pour chaque ligne de la facture est stocké dans la table Lignes_Facture et ne change pas, même si le taux de TVA du produit change dans le futur.

## peuplement.sql
Ensuite le fichier peuplement.sql qui permet de remplir les différentes tables suivant l'exemple donné par le sujet.
Ainsi que 2 fonctions pour remplir automatiquement les lignes de facture et les factures des clients

## api.py

Le fichier api.py est un code permettant de créer une instance Flask avec le code RESTAPI (update,create,get,delete) les tables clients, produits et taux tva.
Le code python est lancé en local avec la commande : python api.py

```
* Serving Flask app 'api'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 389-932-572
```

Grace à l'application "Insomnia" nous pouvons utiliser les différentes fonctions qui permettent de modifier la base de donnée avec du "json".

```
Ex :
http://127.0.0.1:5000/client
En json 
{
	"ID_client":"2",
	"Nom":"Lukas",
	"Adresse": "rue bis, Paris",
	"Email": "lukas@gmail.com",
	"Telephone": "06",
	"Code_IBAN": "FR",
	"Code_BIC_SWIFT": "xxxx"
}
```
