def afficher_heure(tuple_heure):
    global heure_personnalisee
    heure_personnalisee = tuple_heure

# Configuration heure perso
choix_heure = input("Voulez-vous régler une heure personnalisée ? (oui/non) : ")

if choix_heure == "oui":
    h = int(input("Entrez les heures (0-23) : "))
    m = int(input("Entrez les minutes (0-59) : "))
    s = int(input("Entrez les secondes (0-59) : "))
    afficher_heure((h, m, s))