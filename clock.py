import time
import threading
import sys


def format_time(h, m, s, display_mode):
    # Affiche l'heure selon le mode 24h ou 12h (AM/PM)
    if display_mode == "12":
        # Conversion 24h -> 12h + suffixe AM/PM
        if h == 0:
            hour_12 = 12
            suffix = "AM"
        elif 1 <= h <= 11:
            hour_12 = h
            suffix = "AM"
        elif h == 12:
            hour_12 = 12
            suffix = "PM"
        else:  # 13..23
            hour_12 = h - 12
            suffix = "PM"

        return f"{hour_12:02d}:{m:02d}:{s:02d} {suffix}"

    # Mode 24h (par défaut)
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


def set_display_mode(state, mode):
    # Permet de choisir entre 12h et 24h
    if mode not in ("12", "24"):
        raise ValueError("Mode invalide. Utilise : m 12 ou m 24")

    with state["lock"]:
        state["display_mode"] = mode


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
            display_mode = state["display_mode"]

        # Affichage sur une seule ligne (avec mode 12h/24h)
        sys.stdout.write("\rHeure Actuelle : " + format_time(h, m, s, display_mode) + "   ")
        sys.stdout.flush()

        # Vérification du déclenchement de l'alarme
        if alarm is not None and (h, m, s) == alarm:
            print("\n!!! ALARME !!!")
            with state["lock"]:
                state["alarm_time"] = None  # Désactivation après déclenchement

        time.sleep(1)

        with state["lock"]:
            tick_one_second(state)


def command_loop(state):
    # Instructions utilisateur
    print("\nCommandes Disponible :")
    print("  h HH MM SS   -> régler l'heure (exemple : h 16 30 00)")
    print("  a HH MM SS   -> régler l'alarme (exemple : a 06 45 00)")
    print("  m 12         -> mode affichage 12h (AM/PM)")
    print("  m 24         -> mode affichage 24h")
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

        try:
            # Régler l'heure
            if command == "h" and len(parts) == 4:
                hh = int(parts[1])
                mm = int(parts[2])
                ss = int(parts[3])
                set_time(state, (hh, mm, ss))
                print(f"\nHeure réglée à {hh:02d}:{mm:02d}:{ss:02d}")

            # Régler l'alarme
            elif command == "a" and len(parts) == 4:
                hh = int(parts[1])
                mm = int(parts[2])
                ss = int(parts[3])
                set_alarm(state, (hh, mm, ss))
                print(f"\nAlarme réglée à {hh:02d}:{mm:02d}:{ss:02d}")

            # Changer le mode d'affichage (bonus 1)
            elif command == "m" and len(parts) == 2:
                mode = parts[1]
                set_display_mode(state, mode)
                print(f"\nMode d'affichage réglé sur {mode}h")

            else:
                print("Commande inconnue. Exemples : h 16 30 00 / a 06 45 00 / m 12 / m 24 / stop")

        except ValueError as e:
            print(f"Erreur : {e}")


def main():
    now = time.localtime()

    state = {
        "current_time": (now.tm_hour, now.tm_min, now.tm_sec),
        "alarm_time": None,
        "display_mode": "24",  # Bonus 1 : mode par défaut
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
