import time
import threading

# Empêche les accès simultanés entre l'affichage et la saisie clavier
lock = threading.Lock()

def format_time(h, m, s):
    return f"{h:02d}:{m:02d}:{s:02d}"

def set_time(state, new_time):
    h, m, s = new_time

    # Vérification de la validité de l'heure
    if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
        raise ValueError("Heure invalide. Exemple : h 16 30 00")
    
    with state["lock"]:
        state["current_time"] = (h, m, s)

def set_alarm(state, alarm):
    h, m, s = alarm

    # Vérification de la validité de l'alarme
    if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
        raise ValueError("Heure invalide. Exemple : a 06 45 00")
    
    with state["lock"]:
        state["alarm_time"] = (h, m, s)

def tick_one_second(state):
    h, m, s = state["current_time"]

    # Ajout d'une seconde avec gestion des débordements
    s += 1
    if s == 60:
        s = 0
        m += 1
    
    if m == 60: 
        m = 0
        h += 1

    if h == 24:
        h = 0

    state["current_time"] = (h, m, s)

def display_loop(state):

    # Boucle principale d'affichage de l'heure
    while state["running"]:
        with state["lock"]:
            h, m, s = state["current_time"]
            alarm = state["alarm_time"]

        # Affichage sur une seule ligne
        print(format_time(h, m, s), end="\r")

        # Vérification du déclenchement de l'alarme
        if alarm is not None and (h, m, s) == alarm:
            print("!!! ALARME !!!")
            with state["lock"]:
                state["alarm_time"] = None # Désactivation après déclenchemant

        time.sleep(1)

        with state["lock"]:
            tick_one_second(state)

