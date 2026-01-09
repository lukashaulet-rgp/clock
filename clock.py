import time
import sys
import select

def afficher_heure(heure, mode_24h=True):
    h, m, s = heure

    if mode_24h:
        print(f"{h:02d}:{m:02d}:{s:02d}")
    else:
        suffix = "AM" if h < 12 else "PM"
        h12 = h % 12
        if h12 == 0:
            h12 = 12
        print(f"{h12:02d}:{m:02d}:{s:02d} {suffix}")

def regler_alarme():
    h = int(input("Heures alarme : "))
    m = int(input("Minutes alarme : "))
    s = int(input("Secondes alarme : "))
    return (h, m, s)

def lire_commande():
    #Ne bloque pas : lit une commande si l’utilisateur tape quelque chose
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().strip().lower()
    return ""

h = int(input("Heures (0-23) : "))
m = int(input("Minutes (0-59) : "))
s = int(input("Secondes (0-59) : "))
heure = (h, m, s)

alarme = regler_alarme()

choix = input("Mode d'affichage (24/12) [24] : ").strip()
mode_24h = (choix != "12")   # si l’utilisateur tape 12 -> mode 12h, sinon 24h

pause = False
print("Commandes : p = pause/reprendre | q = quitter")

while True:
    afficher_heure(heure, mode_24h)

    cmd = lire_commande()
    if cmd == "p":
        pause = not pause
        print("Pause" if pause else "Reprise")
    elif cmd == "q":
        print("Arrêt.")
        break

    if alarme is not None and heure == alarme:
        print("ALARME !")
        alarme = None

    time.sleep(1)

    if not pause:
        h, m, s = heure
        s += 1
        if s == 60:
            s = 0
            m += 1
        if m == 60:
            m = 0
            h += 1
        if h == 24:
            h = 0
        heure = (h, m, s)



       

        








