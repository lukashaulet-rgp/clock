import time
while True:
    t = time.localtime()
    h = t.tm_hour
    m = t.tm_min
    s = t.tm_sec

    print(f"{h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)

    def afficher_heure(heure):
        h, m, s = heure
        print(f"{h:02d}:{m:02d}:{s:02d}")

    while True:
        t = time.localtime()
        heure = (t.tm_hour, t.tm_min, t.tm_sec)

        afficher_heure(heure)
        time.sleep(1)

