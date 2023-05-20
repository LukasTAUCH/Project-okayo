from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)                                                        # Creer une instance Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/okayo'  # Pour de connecter l instance à ma base de données
db = SQLAlchemy(app)                                                         # Permet d initialiser un nouveau objet SQLAlchemy
ma = Marshmallow(app)                                                        # Initialise l objet Marshmallow


############################# APIREST CLIENTS ########################################################################################################################
# Models
class Clients(db.Model):                                                     # Crée une classe de la meme forme que ma table 
    ID_Client = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255), nullable=False)
    Adresse = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Telephone = db.Column(db.String(20), nullable=False)
    Code_IBAN = db.Column(db.String(34), nullable=False)
    Code_BIC_SWIFT = db.Column(db.String(11), nullable=False)

# Schemas
class ClientSchema(ma.SQLAlchemyAutoSchema):                                # class qui hérite de la classe SQLAlchemyAutoSchema 
    class Meta:                                                             # classe interne pour obtenir des informations supplementaires sur la classe ClientSchema
        model = Clients                                                     # model de la classe Meta est défini sur Clients donc la classe ClientSchema va pouvoir generer automatiquement des champs basés sur les colonnes de la table Clients de notre base de données

# Mise en variable des schemas
client_schema = ClientSchema()             
clients_schema = ClientSchema(many=True)

# Les différentes fonctions
@app.route("/client", methods=["POST"])                                    # Permet d'ajouter un client (en json via Insomnia logiciel) (grace a la method POST)
def add_client():
    new_client = Clients(
        ID_Client=request.json['ID_client'],
        Nom=request.json['Nom'],
        Adresse=request.json['Adresse'],
        Email=request.json['Email'],
        Telephone=request.json['Telephone'],
        Code_IBAN=request.json['Code_IBAN'],
        Code_BIC_SWIFT=request.json['Code_BIC_SWIFT'],
    )
    db.session.add(new_client)
    db.session.commit()
    return client_schema.jsonify(new_client)

@app.route("/client", methods=["GET"])                                  # Permet avec la method Get d avoir toutes les infos de tous les clients dans ma base de données
def get_clients():
    all_clients = Clients.query.all()
    return clients_schema.jsonify(all_clients)

@app.route("/client/<id>", methods=["GET"])                             # Permet d avoir les informations d'un client particulier grace a un id particulier
def get_client(id):
    client = Clients.query.get(id)
    return client_schema.jsonify(client)

@app.route("/client/<id>", methods=["PUT"])                             # Update la table d'un client en fonction de son id 
def update_client(id):
    client = Clients.query.get(id)
    client.Nom = request.json['Nom']
    client.Adresse = request.json['Adresse']
    client.Email = request.json['Email']
    client.Telephone = request.json['Telephone']
    client.Code_IBAN = request.json['Code_IBAN']
    client.Code_BIC_SWIFT = request.json['Code_BIC_SWIFT']
    db.session.commit()
    return client_schema.jsonify(client)

@app.route("/client/<id>", methods=["DELETE"])                        # Permet d effacer un client 
def delete_client(id):
    client = Clients.query.get(id)
    db.session.delete(client)
    db.session.commit()
    return client_schema.jsonify(client)

############################# APIREST PRODUITS ########################################################################################################################

class Produits(db.Model):
    ID_Produit = db.Column(db.Integer, primary_key=True)
    Nom_Produit = db.Column(db.String(255), nullable=False)
    Prix_Unitaire_HT = db.Column(db.Numeric(10, 2), nullable=False)

class ProduitsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produits

produits_schema = ProduitsSchema()
produits_list_schema = ProduitsSchema(many=True)

@app.route("/produit", methods=["POST"])
def add_produit():
    new_produit = Produits(
        ID_Produit=request.json['ID_Produit'],
        Nom_Produit=request.json['Nom_Produit'],
        Prix_Unitaire_HT=request.json['Prix_Unitaire_HT'],
    )
    db.session.add(new_produit)
    db.session.commit()
    return produits_schema.jsonify(new_produit)

@app.route("/produit", methods=["GET"])
def get_produits():
    all_produits = Produits.query.all()
    return produits_list_schema.jsonify(all_produits)

@app.route("/produit/<id>", methods=["GET"])
def get_produit(id):
    produit = Produits.query.get(id)
    return produits_schema.jsonify(produit)

@app.route("/produit/<id>", methods=["PUT"])
def update_produit(id):
    produit = Produits.query.get(id)

    if not produit:
        return {"message": "Product not found"}, 404

    produit.Nom_Produit = request.json.get('Nom_Produit', produit.Nom_Produit)
    produit.Prix_Unitaire_HT = request.json.get('Prix_Unitaire_HT', produit.Prix_Unitaire_HT)

    db.session.commit()
    return produits_schema.jsonify(produit)

@app.route("/produit/<id>", methods=["DELETE"])
def delete_produit(id):
    produit = Produits.query.get(id)

    if not produit:
        return {"message": "Product not found"}, 404

    db.session.delete(produit)
    db.session.commit()
    return produits_schema.jsonify(produit)

############################# APIREST TAUX_TVA ########################################################################################################################

class Taux_TVA(db.Model):
    ID_Taux_TVA = db.Column(db.Integer, primary_key=True)
    Taux_TVA = db.Column(db.Numeric(4, 2), nullable=False)
    Date_Debut = db.Column(db.Date, nullable=False)
    Date_Fin = db.Column(db.Date, nullable=True)  # this can be null if the tax rate is current
    ID_Produit = db.Column(db.Integer, db.ForeignKey('produits.ID_Produit'), nullable=False)

class Taux_TVASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Taux_TVA

taux_tva_schema = Taux_TVASchema()
taux_tva_list_schema = Taux_TVASchema(many=True)        

@app.route("/taux_tva", methods=["POST"])
def add_taux_tva():
    new_taux_tva = Taux_TVA(
        ID_Taux_TVA=request.json['ID_Taux_TVA'],
        Taux_TVA=request.json['Taux_TVA'],
        Date_Debut=request.json['Date_Debut'],
        Date_Fin=request.json.get('Date_Fin'),  # this can be null
        ID_Produit=request.json['ID_Produit'],
    )
    db.session.add(new_taux_tva)
    db.session.commit()
    return taux_tva_schema.jsonify(new_taux_tva)

@app.route("/taux_tva", methods=["GET"])
def get_taux_tva():
    all_taux_tva = Taux_TVA.query.all()
    return taux_tva_list_schema.jsonify(all_taux_tva)

@app.route("/taux_tva/<id>", methods=["GET"])
def get_single_taux_tva(id):
    taux_tva = Taux_TVA.query.get(id)
    return taux_tva_schema.jsonify(taux_tva)

@app.route("/taux_tva/<id>", methods=["PUT"])
def update_taux_tva(id):
    taux_tva = Taux_TVA.query.get(id)

    if not taux_tva:
        return {"message": "Tax rate not found"}, 404

    taux_tva.Taux_TVA = request.json.get('Taux_TVA', taux_tva.Taux_TVA)
    taux_tva.Date_Debut = request.json.get('Date_Debut', taux_tva.Date_Debut)
    taux_tva.Date_Fin = request.json.get('Date_Fin', taux_tva.Date_Fin)
    taux_tva.ID_Produit = request.json.get('ID_Produit', taux_tva.ID_Produit)

    db.session.commit()
    return taux_tva_schema.jsonify(taux_tva)

@app.route("/taux_tva/<id>", methods=["DELETE"])
def delete_taux_tva(id):
    taux_tva = Taux_TVA.query.get(id)

    if not taux_tva:
        return {"message": "Tax rate not found"}, 404

    db.session.delete(taux_tva)
    db.session.commit()
    return taux_tva_schema.jsonify(taux_tva)

#############################################################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
