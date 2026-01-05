import time

def afficher_heure(heure):
        h, m, s = heure
        print(f"{h:02d}:{m:02d}:{s:02d}")

h = int(input("Heures (0-23) : "))
m = int(input("Minutes (0-59) : "))
s = int(input("Secondes (0-59) : "))

heure = (h, m, s)

while True:
        afficher_heure(heure)
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


