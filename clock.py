import time

def afficher_heure(heure):
        h, m, s = heure
        print(f"{h:02d}:{m:02d}:{s:02d}")

def regler_alarme():
        h = int(input("Heures alarme : "))
        m = int(input("Minutes alarme : "))
        s = int(input("Secondes alarme : "))
        return (h, m, s)

h = int(input("Heures (0-23) : "))
m = int(input("Minutes (0-59) : "))
s = int(input("Secondes (0-59) : "))

heure = (h, m, s)
alarme = regler_alarme()

while True:
        afficher_heure(heure)

        if alarme is not None and heure == alarme:
            print("⏰ ALARME !")
            alarme = None

        time.sleep(1)

        h, m, s = heure
        s = s + 1

        if s == 60:
                s = 0
                m = m + 1
        if m == 60:
                m = 0
                h = h + 1
        if h == 24:
                h = 0
        heure = (h, m, s)

       

        








