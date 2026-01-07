import time
import threading
import sys

def format_time(h, m, s, display_mode):
    # Affiche l'heure selon le mode 24h ou 12h (AM/PM)
    if display_mode == "12":
        if h == 0:
            hour_12 = 12
            suffix = "AM"
        elif 1 <= h <= 11:
            hour_12 = h
            suffix = "AM"
        elif h == 12:
            hour_12 = 12
            suffix = "PM"
        else:
            hour_12 = h - 12
            suffix = "PM"

        return f"{hour_12:02d}:{m:02d}:{s:02d} {suffix}"

    return f"{h:02d}:{m:02d}:{s:02d}"


def set_time(state, new_time):
    h, m, s = new_time

    if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
        raise ValueError("Heure invalide. Exemple : h 16 30 00")

    with state["lock"]:
        state["current_time"] = (h, m, s)


def set_alarm(state, alarm):
    h, m, s = alarm

    if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
        raise ValueError("Heure invalide. Exemple : a 06 45 00")

    with state["lock"]:
        state["alarm_time"] = (h, m, s)


def set_display_mode(state, mode):
    if mode not in ("12", "24"):
        raise ValueError("Mode invalide. Utilise : m 12 ou m 24")

    with state["lock"]:
        state["display_mode"] = mode


def tick_one_second(state):
    h, m, s = state["current_time"]

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
    while state["running"]:
        with state["lock"]:
            h, m, s = state["current_time"]
            alarm = state["alarm_time"]
            display_mode = state["display_mode"]
            paused = state["paused"]

        sys.stdout.write(
            "\rHeure Actuelle : "
            + format_time(h, m, s, display_mode)
            + (" PAUSE " if paused else "        ")
        )
        sys.stdout.flush()

        if alarm is not None and (h, m, s) == alarm:
            print("\n!!! ALARME !!!")
            with state["lock"]:
                state["alarm_time"] = None

        time.sleep(1)

        with state["lock"]:
            if not state["paused"]:
                tick_one_second(state)


def command_loop(state):
    print("\nCommandes Disponibles :")
    print("  h HH MM SS   -> régler l'heure (ex : h 16 30 00)")
    print("  a HH MM SS   -> régler l'alarme (ex : a 06 45 00)")
    print("  m 12         -> mode affichage 12h (AM/PM)")
    print("  m 24         -> mode affichage 24h")
    print("  pause        -> mettre l'horloge en pause")
    print("  resume       -> relancer l'horloge")
    print("  stop         -> arrêt du programme\n")

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

        try:
            parts = line.split()
            command = parts[0].lower()

            if command == "h" and len(parts) == 4:
                set_time(state, (int(parts[1]), int(parts[2]), int(parts[3])))
                print("\nHeure réglée")

            elif command == "a" and len(parts) == 4:
                set_alarm(state, (int(parts[1]), int(parts[2]), int(parts[3])))
                print("\nAlarme réglée")

            elif command == "m" and len(parts) == 2:
                set_display_mode(state, parts[1])
                print(f"\nMode d'affichage réglé sur {parts[1]}h")

            elif line.lower() == "pause":
                with state["lock"]:
                    state["paused"] = True
                print("\nHorloge mise en pause")

            elif line.lower() == "resume":
                with state["lock"]:
                    state["paused"] = False
                print("\nHorloge relancée")

            else:
                print("Commande inconnue")

        except ValueError as e:
            print(f"Erreur : {e}")


def main():
    now = time.localtime()

    state = {
        "current_time": (now.tm_hour, now.tm_min, now.tm_sec),
        "alarm_time": None,
        "display_mode": "24",
        "paused": False,   # BONUS 2
        "running": True,
        "lock": threading.Lock(),
    }

    t = threading.Thread(target=display_loop, args=(state,), daemon=True)
    t.start()

    command_loop(state)

    print("Arrêt ...")
    time.sleep(0.2)


if __name__ == "__main__":
    main()
