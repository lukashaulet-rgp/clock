def regler_alarme(tuple_heure):
    global alarme
    alarme = tuple_heure

# Configuration alarme
choix_alarme = input("Voulez-vous régler une alarme ? (oui/non) : ")

if choix_alarme == "oui":
    h = int(input("Entrez les heures de l'alarme (0-23) : "))
    m = int(input("Entrez les minutes de l'alarme (0-59) : "))
    s = int(input("Entrez les secondes de l'alarme (0-59) : "))
    regler_alarme((h, m, s))