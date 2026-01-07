import time 
from datetime import datetime

# Variables globales
heure_personnalisee = None
alarme = None


# Fonction pour régler une h perso
def afficher_heure(tuple_heure):
    global heure_personnalisee
    heure_personnalisee = tuple_heure


# Fonction pour régler l'alarme
def regler_alarme(tuple_heure):
    global alarme
    alarme = tuple_heure


# Fonction pour ajouter 1 seconde à l'heure
def incrementer_heure(h, m, s):
    s = s + 1
    
    if s >= 60:
        s = 0
        m = m + 1
    
    if m >= 60:
        m = 0
        h = h + 1
    
    if h >= 24:
        h = 0
    
    return (h, m, s)


# Fonction pour arrêter l'horloge proprement
def arreter_horloge():
    print("\n")
    print("Horloge arrêtée. A bientôt Mamie Jeannine !")


# Intituler
print("=== HORLOGE POUR MAMI ===")
print("")

# dispo pour une h perso
choix_heure = input("Voulez-vous régler une heure personnalisée ? (oui/non) : ")

if choix_heure == "oui":
    h = int(input("Entrez les heures (0-23) : "))
    m = int(input("Entrez les minutes (0-59) : "))
    s = int(input("Entrez les secondes (0-59) : "))
    afficher_heure((h, m, s))

# Dispo pour une alarme
choix_alarme = input("Voulez-vous régler une alarme ? (oui/non) : ")

if choix_alarme == "oui":
    h = int(input("Entrez les heures de l'alarme (0-23) : "))
    m = int(input("Entrez les minutes de l'alarme (0-59) : "))
    s = int(input("Entrez les secondes de l'alarme (0-59) : "))
    regler_alarme((h, m, s))

print("")
print("Horloge en cours... (Ctrl+C pour arrêter)")
print("")

# Boucle qui tourne à l'infini avec gestion de l'arrêt
try:
    while True:
        
        if heure_personnalisee is not None:
            heures, minutes, secondes = heure_personnalisee
            heure_personnalisee = incrementer_heure(heures, minutes, secondes)
        else:
            maintenant = datetime.now()
            heures = maintenant.hour
            minutes = maintenant.minute
            secondes = maintenant.second
        
        print(f"\r{heures:02d}:{minutes:02d}:{secondes:02d}", end="", flush=True)
        
        if alarme is not None:
            if (heures, minutes, secondes) == alarme:
                print("\nDRIIIING ! C'est l'heure Mamie Jeannine !")
        
        time.sleep(1)

# Quand on appuie sur Ctrl+C, on arrête proprement
except KeyboardInterrupt:
    arreter_horloge()