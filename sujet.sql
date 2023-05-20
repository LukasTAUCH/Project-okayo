
USE okayo;  

# DROP TABLE IF EXISTS Lignes_Facture;
# DROP TABLE IF EXISTS Factures;
# DROP TABLE IF EXISTS Taux_TVA;
# DROP TABLE IF EXISTS Produits;
# DROP TABLE IF EXISTS Clients;

# une PRIMARY KEY est unique pour chaque table
# une FOREIGNE KEY permet de faire référence à un certaine PRIMARY KEY d'une autre table et donc permet la liaison de la TABLE aux differents individus de l'autre TABLE


CREATE TABLE Clients (
  ID_Client INT PRIMARY KEY,
  Nom VARCHAR(255),
  Adresse VARCHAR(255),
  Email VARCHAR(255),
  Telephone VARCHAR(20),
  Code_IBAN VARCHAR(34),
  Code_BIC_SWIFT VARCHAR(11) 
);

CREATE TABLE Produits (
  ID_Produit INT PRIMARY KEY,
  Nom_Produit VARCHAR(255),
  Prix_Unitaire_HT DECIMAL(10, 2)
);

CREATE TABLE Taux_TVA (
  ID_Taux_TVA INT PRIMARY KEY,
  Taux_TVA DECIMAL(4, 2),
  Date_Debut DATE,
  Date_Fin DATE,
  ID_Produit INT,
  FOREIGN KEY (ID_Produit) REFERENCES Produits(ID_Produit)
);

CREATE TABLE Factures (
  ID_Facture INT PRIMARY KEY,
  Date_Facture DATE,
  ID_Client INT,
  Total_HT DECIMAL(10, 2),
  Total_TVA DECIMAL(10, 2),
  Total_TTC DECIMAL(10, 2),
  FOREIGN KEY (ID_Client) REFERENCES Clients(ID_Client)
);

CREATE TABLE Lignes_Facture (
  ID_Ligne_Facture INT PRIMARY KEY,
  ID_Facture INT,
  ID_Produit INT,
  Quantite INT,
  Prix_Unitaire_HT DECIMAL(10, 2),
  Taux_TVA DECIMAL(4, 2),
  Total_HT DECIMAL(10, 2),
  Total_TVA DECIMAL(10, 2),
  FOREIGN KEY (ID_Facture) REFERENCES Factures(ID_Facture),
  FOREIGN KEY (ID_Produit) REFERENCES Produits(ID_Produit)
);


/* 
Avec ces tables :
- Chaque client peut avoir plusieurs factures
- Chaque facture peut avoir plusieurs lignes de factures
- Chaque ligne correspond à un produit spécifique 
- Chaque produit peut avoir un taux TVA associé
- Chaque tables sont liées par des clés étrangères pour assurer l'intégrité des données
