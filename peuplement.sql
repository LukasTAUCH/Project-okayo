INSERT INTO Clients (ID_Client, Nom, Adresse, Email, Telephone, Code_IBAN, Code_BIC_SWIFT)
VALUES (1, 'Okayo', '45, rue du test, 75016 PARIS', 'sas@okayo.fr', '01 80 88 63 00', 'FR76 0000 0000 0000 0000 0000 097', 'BREDFRPPXXX');

INSERT INTO Produits (ID_Produit, Nom_Produit, Prix_Unitaire_HT)
VALUES (1, 'Mon produit C', 70000.00),
       (2, 'Mon produit A', 1500.00),
       (3, 'Mon produit D', 3000.00),
       (4, 'Mon produit B', 4000.00);

INSERT INTO Taux_TVA (ID_Taux_TVA, Taux_TVA, ID_Produit)
VALUES (1, 20.00, 1),
       (2, 5.50, 2),
       (3, 20.00, 3),
       (4, 7.00, 4);

# Nous voulons automatiser l'insertion avec des fonctions
INSERT INTO Factures (ID_Facture, Date_Facture, ID_Client, Total_HT, Total_TVA, Total_TTC)
VALUES (1, '2023-05-19', 1, 84000.00, 15325.00, 99325.00);

INSERT INTO Lignes_Facture (ID_Ligne_Facture, ID_Facture, ID_Produit, Quantite, Prix_Unitaire_HT, Taux_TVA, Total_HT, Total_TVA)
VALUES (1, 1, 1, 1, 70000.00, 20.00, 70000.00, 14000.00),
       (2, 1, 2, 2, 1500.00, 5.50, 3000.00, 165.00),
       (3, 1, 3, 1, 3000.00, 20.00, 3000.00, 600.00),
       (4, 1, 4, 2, 4000.00, 7.00, 8000.00, 560.00);

# Fonction pour remplir automatiquement la table Lignes_Facture 

# iL faut que l Id facture existe meme si cette derniere n'est pas rempli

# DROP PROCEDURE IF EXISTS AddLigneFacture;
DELIMITER //
CREATE PROCEDURE AddLigneFacture(IN param_id_ligne_facture INT, IN param_id_facture INT, IN param_id_produit INT, IN param_quantite INT)
BEGIN
    INSERT INTO Lignes_Facture (ID_Ligne_Facture, ID_Facture, ID_Produit, Quantite, Prix_Unitaire_HT, Taux_TVA, Total_HT, Total_TVA)
    SELECT param_id_ligne_facture, param_id_facture, p.ID_Produit, param_quantite, p.Prix_Unitaire_HT, t.Taux_TVA, 
           p.Prix_Unitaire_HT * param_quantite, p.Prix_Unitaire_HT * param_quantite * (t.Taux_TVA / 100)
    FROM Produits p
    INNER JOIN Taux_TVA t ON p.ID_Produit = t.ID_Produit
    WHERE p.ID_Produit = param_id_produit;
END //
DELIMITER ;

# exemple 
INSERT INTO Factures (ID_Facture, Date_Facture, ID_Client) VALUES (1, '2023-05-19', 1);      -- Ici on crée une facture mais n ayant pas de valeurs pour l instant

# Création des lignes de facture en fonction d'une facture particulière
CALL AddLigneFacture(1, 1, 1, 1); 
CALL AddLigneFacture(2, 1, 2, 2); 
CALL AddLigneFacture(3, 1, 3, 1); 
CALL AddLigneFacture(4, 1, 4, 2); 


# DROP PROCEDURE IF EXISTS AddFacture;
DELIMITER //
CREATE PROCEDURE AddFacture(IN param_id_facture INT, IN param_date_facture DATE, IN param_id_client INT)
BEGIN
    UPDATE Factures
    SET Date_Facture = param_date_facture, 
        ID_Client = param_id_client, 
        Total_HT = (SELECT SUM(Total_HT) FROM Lignes_Facture WHERE ID_Facture = param_id_facture),
        Total_TVA = (SELECT SUM(Total_TVA) FROM Lignes_Facture WHERE ID_Facture = param_id_facture),
        Total_TTC = (SELECT SUM(Total_HT + Total_TVA) FROM Lignes_Facture WHERE ID_Facture = param_id_facture)
    WHERE ID_Facture = param_id_facture;
END //
DELIMITER ;

# Exemple 
CALL AddFacture(1, '2023-05-19', 1); -- Mise à jour de la facture avec le Total HT Total TVA et Total TTC

