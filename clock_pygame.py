import math
import time
import pygame
import pygame.gfxdraw

# -----------------------------
# Helpers
# -----------------------------
def polar_to_xy(cx, cy, radius, angle_rad):
    """0 rad = en haut (12h). Sens horaire."""
    x = cx + radius * math.sin(angle_rad)
    y = cy - radius * math.cos(angle_rad)
    return int(x), int(y)

def draw_aa_circle(surface, x, y, r, color):
    pygame.gfxdraw.aacircle(surface, x, y, r, color)
    pygame.gfxdraw.filled_circle(surface, x, y, r, color)

def draw_aa_ring(surface, x, y, r, thickness, color):
    for i in range(thickness):
        pygame.gfxdraw.aacircle(surface, x, y, r - i, color)

def draw_hand(surface, cx, cy, angle, length, width, color, tail=0):
    dx = math.sin(angle)
    dy = -math.cos(angle)
    px = -dy
    py = dx

    x1 = cx + dx * length
    y1 = cy + dy * length
    x0 = cx - dx * tail
    y0 = cy - dy * tail

    w = width / 2.0
    p1 = (x0 + px * w, y0 + py * w)
    p2 = (x0 - px * w, y0 - py * w)
    p3 = (x1 - px * w * 0.65, y1 - py * w * 0.65)
    p4 = (x1 + px * w * 0.65, y1 + py * w * 0.65)

    pygame.draw.polygon(surface, color, [p1, p2, p3, p4])

def clamp(v, a, b):
    return max(a, min(b, v))

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

def parse_hms(s):
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

# -----------------------------
# UI
# -----------------------------
class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, screen, mouse_pos, gold, border):
        hovered = self.rect.collidepoint(mouse_pos)
        bg = (45, 45, 48) if not hovered else (60, 60, 65)
        pygame.draw.rect(screen, bg, self.rect, border_radius=12)
        pygame.draw.rect(screen, border, self.rect, 2, border_radius=12)
        label = self.font.render(self.text, True, gold)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class TextBox:
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
                return
            else:
                if len(self.text) < self.max_len:
                    ch = event.unicode
                    if ch.isdigit() or ch in (" ", ":"):
                        self.text += ch

    def draw(self, screen, gold, border):
        bg = (30, 30, 33) if not self.active else (40, 40, 44)
        pygame.draw.rect(screen, bg, self.rect, border_radius=10)
        pygame.draw.rect(screen, border, self.rect, 2, border_radius=10)

        show = self.text if self.text else self.placeholder
        col = (235, 235, 235) if self.text else (160, 160, 160)
        label = self.font.render(show, True, col)
        screen.blit(label, (self.rect.x + 10, self.rect.y + (self.rect.height - label.get_height()) // 2))

    def clear(self):
        self.text = ""

    def get_value(self):
        return self.text.strip()

# -----------------------------
# Main
# -----------------------------
def main():
    pygame.init()
    pygame.display.set_caption("Horloge Moderne (noir/or) - complète")

    W, H = 1100, 720
    screen = pygame.display.set_mode((W, H))
    fps = pygame.time.Clock()

    # Couleurs (style photo)
    BG = (12, 12, 14)
    DIAL = (28, 28, 30)
    DIAL_SHADE = (22, 22, 24)
    GOLD = (200, 170, 95)
    GOLD_DIM = (150, 125, 70)
    BORDER = (85, 85, 90)
    WHITE_SOFT = (235, 235, 235)

    # Fonts
    font_title = pygame.font.SysFont("Segoe UI", 22)
    font = pygame.font.SysFont("Segoe UI", 20)
    font_small = pygame.font.SysFont("Segoe UI", 18)
    font_big = pygame.font.SysFont("Segoe UI", 36)

    # Position horloge
    cx, cy = 420, H // 2 + 10
    radius = 260

    # Surface cadran (pré-rendu)
    dial_surf = pygame.Surface((radius * 2 + 80, radius * 2 + 80), pygame.SRCALPHA)
    dcx, dcy = dial_surf.get_width() // 2, dial_surf.get_height() // 2

    def build_dial():
        dial_surf.fill((0, 0, 0, 0))

        # Ombre douce
        shadow_off = 10
        draw_aa_circle(dial_surf, dcx + shadow_off, dcy + shadow_off, radius + 6, (0, 0, 0, 120))

        # Cadran
        draw_aa_circle(dial_surf, dcx, dcy, radius, DIAL)

        # Vignettage
        for i in range(24):
            rr = radius - i * 6
            alpha = clamp(int(35 - i * 1.4), 0, 35)
            pygame.gfxdraw.aacircle(dial_surf, dcx, dcy, rr, (*DIAL_SHADE, alpha))

        # Bordure
        draw_aa_ring(dial_surf, dcx, dcy, radius, 2, (55, 55, 58))
        draw_aa_ring(dial_surf, dcx, dcy, radius - 3, 1, (45, 45, 48))

        # Index dorés
        for i in range(12):
            ang = i * (2 * math.pi / 12)
            outer_r = radius - 14
            inner_r = radius - 42
            x_out, y_out = polar_to_xy(dcx, dcy, outer_r, ang)
            x_in, y_in = polar_to_xy(dcx, dcy, inner_r, ang)

            is_quarter = (i % 3 == 0)
            bar_w = 8 if is_quarter else 6

            dx = math.sin(ang)
            dy = -math.cos(ang)
            px = -dy
            py = dx
            w = bar_w / 2

            p1 = (x_in + px*w, y_in + py*w)
            p2 = (x_in - px*w, y_in - py*w)
            p3 = (x_out - px*w, y_out - py*w)
            p4 = (x_out + px*w, y_out + py*w)

            shadow = [(p1[0]+1, p1[1]+1), (p2[0]+1, p2[1]+1), (p3[0]+1, p3[1]+1), (p4[0]+1, p4[1]+1)]
            pygame.draw.polygon(dial_surf, (0, 0, 0, 70), shadow)
            pygame.draw.polygon(dial_surf, GOLD, [p1, p2, p3, p4])
            pygame.draw.polygon(dial_surf, GOLD_DIM, [p1, p2, p3, p4], 1)

        # Centre
        draw_aa_circle(dial_surf, dcx, dcy, 10, (40, 40, 42))
        draw_aa_ring(dial_surf, dcx, dcy, 10, 2, (80, 80, 85))
        draw_aa_circle(dial_surf, dcx, dcy, 4, GOLD)

    build_dial()

    # État horloge (initial = heure système)
    lt = time.localtime()
    cur_h, cur_m, cur_s = lt.tm_hour, lt.tm_min, lt.tm_sec

    display_mode = "24"
    paused = False
    alarm = None  # tuple (h,m,s)

    # tick 1 seconde (logique)
    last_tick_ms = pygame.time.get_ticks()

    # -----------------------------
    # UI panel à droite (layout auto)
    # -----------------------------
    panel_x = 740
    panel_w = 330
    panel_rect = pygame.Rect(panel_x, 90, panel_w, 560)

    pad = 18
    gap = 12
    y = panel_rect.y + 70  # après le titre "Réglages"

    def row(h):
        nonlocal y
        r = pygame.Rect(panel_x + pad, y, panel_w - 2 * pad, h)
        y += h + gap
        return r

    tb_time = TextBox(row(44), "Régler l'heure: HH MM SS", font_small)
    btn_apply_time = Button(row(44), "Appliquer l'heure", font_small)

    tb_alarm = TextBox(row(44), "Régler l'alarme: HH MM SS", font_small)
    btn_apply_alarm = Button(row(44), "Appliquer l'alarme", font_small)

    y += 10

    half_w = (panel_w - 2 * pad - gap) // 2
    btn_pause = Button((panel_x + pad, y, half_w, 48), "Pause", font_small)
    btn_resume = Button((panel_x + pad + half_w + gap, y, half_w, 48), "Reprendre", font_small)
    y += 48 + gap

    btn_toggle = Button(row(48), "Mode 12/24", font_small)
    btn_clear_alarm = Button(row(48), "Désactiver l'alarme", font_small)

    status_y = panel_rect.bottom - 70

    message = "Clique dans un champ, tape HH MM SS, puis Entrée ou bouton."
    message_until = 0
    alarm_popup_until = 0

    # --- Quit confirmation + fade-out ---
    quit_confirm = False
    fading_out = False
    fade_alpha = 0
    FADE_SPEED = 12  # plus grand = plus rapide

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        now_ms = pygame.time.get_ticks()

        # tick logique: toutes les 1000 ms
        if not paused and (now_ms - last_tick_ms) >= 1000:
            steps = (now_ms - last_tick_ms) // 1000
            for _ in range(int(steps)):
                cur_h, cur_m, cur_s = tick_one_second(cur_h, cur_m, cur_s)

                if alarm is not None and (cur_h, cur_m, cur_s) == alarm:
                    alarm = None
                    alarm_popup_until = now_ms + 4500
                    message = "!!! ALARME !!!"
                    message_until = now_ms + 4500

            last_tick_ms += int(steps) * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_confirm = True

            # Quitter avec confirmation (solution recommandée = KEYDOWN)
            if event.type == pygame.KEYDOWN:
                # Si on est dans la confirmation
                if quit_confirm and not fading_out:
                    if event.key in (pygame.K_y, pygame.K_RETURN):   # Oui
                        fading_out = True
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE): # Non
                        quit_confirm = False

                # Si on n'est PAS dans la confirmation
                elif not quit_confirm and not fading_out:
                    if event.key == pygame.K_ESCAPE:
                        quit_confirm = True

            # Tant qu'on est dans la confirmation (et pas en fade),
            # on bloque le reste des interactions
            if quit_confirm and not fading_out:
                continue

            tb_time.handle_event(event)
            tb_alarm.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    if tb_time.active:
                        h, m, s = parse_hms(tb_time.get_value())
                        cur_h, cur_m, cur_s = h, m, s
                        last_tick_ms = pygame.time.get_ticks()
                        tb_time.clear()
                        message = "Heure réglée."
                        message_until = now_ms + 2500
                    elif tb_alarm.active:
                        h, m, s = parse_hms(tb_alarm.get_value())
                        alarm = (h, m, s)
                        tb_alarm.clear()
                        message = "Alarme réglée."
                        message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

            if btn_apply_time.clicked(event):
                try:
                    h, m, s = parse_hms(tb_time.get_value())
                    cur_h, cur_m, cur_s = h, m, s
                    last_tick_ms = pygame.time.get_ticks()
                    tb_time.clear()
                    message = "Heure réglée."
                    message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

            if btn_apply_alarm.clicked(event):
                try:
                    h, m, s = parse_hms(tb_alarm.get_value())
                    alarm = (h, m, s)
                    tb_alarm.clear()
                    message = "Alarme réglée."
                    message_until = now_ms + 2500
                except ValueError as e:
                    message = f"Erreur: {e}"
                    message_until = now_ms + 3500

            if btn_pause.clicked(event):
                paused = True
                message = "Horloge en pause."
                message_until = now_ms + 2500

            if btn_resume.clicked(event):
                paused = False
                last_tick_ms = pygame.time.get_ticks()
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

        # Render
        screen.fill(BG)

        # Header
        screen.blit(font_title.render("Horloge moderne (noir/or) — complète", True, (210, 210, 210)), (24, 18))

        # Cadran
        dial_rect = dial_surf.get_rect(center=(cx, cy))
        screen.blit(dial_surf, dial_rect)

        # Angle "fluide" des secondes pour l'affichage
        # IMPORTANT: on aligne la fraction de seconde sur le tick interne (last_tick_ms),
        # sinon l'aiguille des secondes "saute" quand cur_s change.
        frac = 0.0
        if not paused:
            frac = (now_ms - last_tick_ms) / 1000.0
            if frac < 0.0:
                frac = 0.0
            if frac > 0.999:
                frac = 0.999
        sec_display = cur_s + frac

        hour12 = cur_h % 12
        ang_s = (sec_display / 60.0) * 2 * math.pi
        ang_m = ((cur_m + sec_display / 60.0) / 60.0) * 2 * math.pi
        ang_h = ((hour12 + (cur_m / 60.0)) / 12.0) * 2 * math.pi

        draw_hand(screen, cx, cy, ang_h, length=140, width=14, color=GOLD, tail=22)
        draw_hand(screen, cx, cy, ang_m, length=195, width=10, color=GOLD, tail=28)

        draw_hand(screen, cx + 1, cy + 1, ang_s, length=220, width=4, color=(0, 0, 0, 90), tail=35)
        draw_hand(screen, cx, cy, ang_s, length=220, width=4, color=GOLD, tail=35)

        draw_aa_circle(screen, cx, cy, 14, (35, 35, 37))
        draw_aa_ring(screen, cx, cy, 14, 2, (90, 90, 96))
        draw_aa_circle(screen, cx, cy, 5, GOLD)

        shown = format_time(cur_h, cur_m, cur_s, display_mode)
        screen.blit(font_big.render(shown, True, WHITE_SOFT), (24, 60))

        # Panel
        pygame.draw.rect(screen, (20, 20, 22), panel_rect, border_radius=18)
        pygame.draw.rect(screen, BORDER, panel_rect, 2, border_radius=18)
        screen.blit(font.render("Réglages", True, (220, 220, 220)), (panel_x + pad, panel_rect.y + 20))

        tb_time.draw(screen, GOLD, BORDER)
        btn_apply_time.draw(screen, mouse_pos, GOLD, BORDER)

        tb_alarm.draw(screen, GOLD, BORDER)
        btn_apply_alarm.draw(screen, mouse_pos, GOLD, BORDER)

        btn_pause.draw(screen, mouse_pos, GOLD, BORDER)
        btn_resume.draw(screen, mouse_pos, GOLD, BORDER)

        btn_toggle.draw(screen, mouse_pos, GOLD, BORDER)
        btn_clear_alarm.draw(screen, mouse_pos, GOLD, BORDER)

        # Statuts en bas
        alarm_txt = "Aucune" if alarm is None else f"{alarm[0]:02d}:{alarm[1]:02d}:{alarm[2]:02d}"
        st1 = f"État: {'PAUSE' if paused else 'EN MARCHE'}"
        st2 = f"Alarme: {alarm_txt}"
        screen.blit(font_small.render(st1, True, (170, 170, 170)), (panel_x + pad, status_y))
        screen.blit(font_small.render(st2, True, (170, 170, 170)), (panel_x + pad, status_y + 24))

        # Message bas
        if now_ms < message_until:
            screen.blit(font_small.render(message, True, (235, 235, 235)), (24, H - 35))

        # Popup alarme
        if now_ms < alarm_popup_until:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(220, 220, 660, 200)
            pygame.draw.rect(screen, (35, 35, 37), box, border_radius=18)
            pygame.draw.rect(screen, GOLD, box, 2, border_radius=18)
            text = pygame.font.SysFont("Segoe UI", 72).render("!!! ALARME !!!", True, GOLD)
            screen.blit(text, text.get_rect(center=box.center))

        # Popup confirmation quitter
        if quit_confirm and not fading_out:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            box = pygame.Rect(260, 250, 580, 180)
            pygame.draw.rect(screen, (25, 25, 28), box, border_radius=18)
            pygame.draw.rect(screen, GOLD, box, 2, border_radius=18)

            title = pygame.font.SysFont("Segoe UI", 32).render("Êtes-vous sûr de vouloir quitter ?", True, (235, 235, 235))
            screen.blit(title, title.get_rect(center=(box.centerx, box.y + 55)))

            hint = pygame.font.SysFont("Segoe UI", 20).render("Oui : Entrée / Y     —     Non : N / Échap", True, (190, 190, 190))
            screen.blit(hint, hint.get_rect(center=(box.centerx, box.y + 120)))

        # Fade-out élégant
        if fading_out:
            fade_alpha = min(255, fade_alpha + FADE_SPEED)
            fade = pygame.Surface((W, H))
            fade.fill((0, 0, 0))
            fade.set_alpha(fade_alpha)
            screen.blit(fade, (0, 0))
            if fade_alpha >= 255:
                running = False

        pygame.display.flip()
        fps.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
