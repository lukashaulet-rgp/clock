import time
import pygame


def format_time(h, m, s, display_mode):
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


def is_valid_hms(h, m, s):
    return (0 <= h <= 23) and (0 <= m <= 59) and (0 <= s <= 59)


def tick_one_second(h, m, s):
    s += 1
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        h += 1
    if h == 24:
        h = 0
    return h, m, s


class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, screen, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = (60, 60, 60) if not hovered else (85, 85, 85)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (140, 140, 140), self.rect, 2, border_radius=10)

        label = self.font.render(self.text, True, (235, 235, 235))
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class TextBox:
    """
    Champ de saisie très simple:
    - Clique pour activer
    - Tape au clavier
    - Entrée = valider (on gère ça dans le code principal)
    - Backspace = effacer
    """
    def __init__(self, rect, placeholder, font, max_len=12):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.font = font
        self.text = ""
        self.active = False
        self.max_len = max_len

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            return

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_RETURN:
                # Le main s'occupe de la validation
                return
            else:
                if len(self.text) < self.max_len:
                    ch = event.unicode
                    # autoriser chiffres, espaces, et ':'
                    if ch.isdigit() or ch in (" ", ":"):
                        self.text += ch

    def draw(self, screen):
        bg = (35, 35, 35) if not self.active else (45, 45, 45)
        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        pygame.draw.rect(screen, (140, 140, 140), self.rect, 2, border_radius=8)

        show = self.text if self.text else self.placeholder
        col = (230, 230, 230) if self.text else (160, 160, 160)
        label = self.font.render(show, True, col)
        screen.blit(label, (self.rect.x + 10, self.rect.y + (self.rect.height - label.get_height()) // 2))

    def clear(self):
        self.text = ""

    def get_value(self):
        return self.text.strip()


def parse_hms(s):
    """
    Accepte:
    - "HH MM SS"
    - "HH:MM:SS"
    """
    s = s.strip()
    if not s:
        raise ValueError("Champ vide")

    if ":" in s:
        parts = s.split(":")
    else:
        parts = s.split()

    if len(parts) != 3:
        raise ValueError("Format attendu: HH MM SS ou HH:MM:SS")

    h, m, sec = int(parts[0]), int(parts[1]), int(parts[2])
    if not is_valid_hms(h, m, sec):
        raise ValueError("Heure invalide (0-23 / 0-59 / 0-59)")
    return h, m, sec


def main():
    pygame.init()
    pygame.display.set_caption("Horloge Pygame (Heure / Alarme / Pause / 12-24)")

    W, H = 900, 520
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont(None, 90)
    font = pygame.font.SysFont(None, 28)
    font_small = pygame.font.SysFont(None, 24)

    # état initial = heure système
    now = time.localtime()
    cur_h, cur_m, cur_s = now.tm_hour, now.tm_min, now.tm_sec
    display_mode = "24"
    paused = False
    alarm = None  # (h,m,s) ou None

    # UI
    btn_pause = Button((40, 340, 160, 52), "Pause", font)
    btn_resume = Button((220, 340, 160, 52), "Reprendre", font)
    btn_toggle = Button((400, 340, 160, 52), "Mode 12/24", font)
    btn_clear_alarm = Button((580, 340, 280, 52), "Désactiver l'alarme", font)

    tb_set_time = TextBox((40, 170, 360, 46), "Régler l'heure: HH MM SS", font_small)
    tb_set_alarm = TextBox((40, 250, 360, 46), "Régler l'alarme: HH MM SS", font_small)
    btn_apply_time = Button((420, 170, 200, 46), "Appliquer heure", font_small)
    btn_apply_alarm = Button((420, 250, 200, 46), "Appliquer alarme", font_small)

    message = "Clique dans un champ pour saisir. Entrée valide (ou bouton)."
    message_until = 0
    alarm_popup_until = 0

    # tick 1 seconde (sans dépendre du FPS)
    last_tick_ms = pygame.time.get_ticks()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        now_ms = pygame.time.get_ticks()

        # tick réel: toutes les 1000 ms
        if not paused and (now_ms - last_tick_ms) >= 1000:
            # rattrapage si lag
            steps = (now_ms - last_tick_ms) // 1000
            for _ in range(int(steps)):
                cur_h, cur_m, cur_s = tick_one_second(cur_h, cur_m, cur_s)
                # alarme
                if alarm is not None and (cur_h, cur_m, cur_s) == alarm:
                    alarm = None
                    alarm_popup_until = now_ms + 4500
                    message = "!!! ALARME !!!"
                    message_until = now_ms + 4500
            last_tick_ms += int(steps) * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Textboxes
            tb_set_time.handle_event(event)
            tb_set_alarm.handle_event(event)

            # Validation Enter sur textbox active
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    if tb_set_time.active:
                        h, m, s = parse_hms(tb_set_time.get_value())
                        cur_h, cur_m, cur_s = h, m, s
                        last_tick_ms = pygame.time.get_ticks()  # resync tick
                        tb_set_time.clear()
                        message = "Heure réglée."
                        message_until = now_ms + 2500
                    elif tb_set_alarm.active:
                        h, m, s = parse_hms(tb_set_alarm.get_value())
                        alarm = (h, m, s)
                        tb_set_alarm.clear()
                        message = "Alarme réglée."
                        message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

            # Boutons
            if btn_pause.clicked(event):
                paused = True
                message = "Horloge en pause."
                message_until = now_ms + 2500

            if btn_resume.clicked(event):
                paused = False
                last_tick_ms = pygame.time.get_ticks()  # resync tick
                message = "Horloge relancée."
                message_until = now_ms + 2500

            if btn_toggle.clicked(event):
                display_mode = "12" if display_mode == "24" else "24"
                message = f"Mode d'affichage: {display_mode}h"
                message_until = now_ms + 2500

            if btn_clear_alarm.clicked(event):
                alarm = None
                message = "Alarme désactivée."
                message_until = now_ms + 2500

            if btn_apply_time.clicked(event):
                try:
                    h, m, s = parse_hms(tb_set_time.get_value())
                    cur_h, cur_m, cur_s = h, m, s
                    last_tick_ms = pygame.time.get_ticks()
                    tb_set_time.clear()
                    message = "Heure réglée."
                    message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

            if btn_apply_alarm.clicked(event):
                try:
                    h, m, s = parse_hms(tb_set_alarm.get_value())
                    alarm = (h, m, s)
                    tb_set_alarm.clear()
                    message = "Alarme réglée."
                    message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

        # Draw
        screen.fill((18, 18, 20))

        # Titre
        title = font.render("Horloge", True, (220, 220, 220))
        screen.blit(title, (40, 25))

        # Heure affichée
        t = format_time(cur_h, cur_m, cur_s, display_mode)
        time_surf = font_big.render(t, True, (245, 245, 245))
        screen.blit(time_surf, (40, 70))

        # Statuts
        status = f"Mode: {display_mode}h   |   {'PAUSE' if paused else 'EN MARCHE'}"
        alarm_txt = "Aucune" if alarm is None else f"{alarm[0]:02d}:{alarm[1]:02d}:{alarm[2]:02d}"
        status2 = f"Alarme: {alarm_txt}"

        s1 = font.render(status, True, (200, 200, 200))
        s2 = font.render(status2, True, (200, 200, 200))
        screen.blit(s1, (40, 140))
        screen.blit(s2, (40, 300))

        # Inputs
        tb_set_time.draw(screen)
        tb_set_alarm.draw(screen)

        # Buttons
        btn_apply_time.draw(screen, mouse_pos)
        btn_apply_alarm.draw(screen, mouse_pos)
        btn_pause.draw(screen, mouse_pos)
        btn_resume.draw(screen, mouse_pos)
        btn_toggle.draw(screen, mouse_pos)
        btn_clear_alarm.draw(screen, mouse_pos)

        # Message barre
        if now_ms < message_until:
            msg = font_small.render(message, True, (240, 240, 240))
            screen.blit(msg, (40, 420))

        # Popup alarme
        if now_ms < alarm_popup_until:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(160, 170, 580, 180)
            pygame.draw.rect(screen, (40, 40, 40), box, border_radius=16)
            pygame.draw.rect(screen, (220, 220, 220), box, 2, border_radius=16)
            txt = pygame.font.SysFont(None, 70).render("!!! ALARME !!!", True, (245, 245, 245))
            screen.blit(txt, txt.get_rect(center=box.center))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
