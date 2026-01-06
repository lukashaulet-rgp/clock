import time
import threading


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
        print(f"Heure Actuelle : {format_time(h, m, s)}")

        # Vérification du déclenchement de l'alarme
        if alarm is not None and (h, m, s) == alarm:
            print("!!! ALARME !!!")
            with state["lock"]:
                state["alarm_time"] = None # Désactivation après déclenchemant

        time.sleep(1)

        with state["lock"]:
            tick_one_second(state)

def command_loop(state):

    # Instructions utilisateur
    print("\nCommandes Disponible :")
    print("  h HH MM SS   -> régler l'heure (exemple : h 16 30 00)")
    print("  a HH MM SS   -> régler l'alarme (exemple : a 06 45 00)")
    print("  stop         -> arrêt du programme\n")

    # Boucle commandes clavier
    while state["running"]:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            state["running"] = False
            break

        if not line:
            continue

        if line.lower() == "stop":
            state["running"] = False
            break

        parts = line.split()
        command = parts[0].lower()

        # Traitement des commandes
        if command in ("h", "a") and len(parts) == 4:
            try:
                hh = int(parts[1])
                mm = int(parts[2])
                ss = int(parts[3])

                if command == "h":
                    set_time(state, (hh, mm, ss))
                    print(f"Heure réglée à {hh:02d} : {mm:02d} : {ss:02d}")
                else:
                    set_alarm(state, (hh, mm, ss))
                    print(f"Alarme réglée à {hh:02d} : {mm:02d} : {ss:02d}")
            
            except ValueError:
                print("Erreur : format attendu -> h HH MM SS or a HH MM SS")
        
        else:
            print("Commande inconnue. Exemples : h 16 30 00 / a 06 45 00 / stop")

def main():

    # Etat partagé du programme
    state = {
        "current_time": (16, 30, 0),
        "alarm_time": None,
        "running": True,
        "lock": threading.Lock(),
    }

    # Démarrage de l'affichage de l'horloge dans un thread séparé
    t = threading.Thread(target=display_loop, args=(state,), daemon=True)
    t.start()

    # Gestion des commandes reste le thread principal
    command_loop(state)

    print("Arrêt ...")
    time.sleep(0.2)


if __name__ == "__main__":
    main()