import tkinter as tk
from datetime import datetime
import math
import random

# ========== VARIABLES GLOBALES ==========
heure_personnalisee = None
alarme = None
mode_affichage = "24h"
horloge_en_pause = False
alarme_active = False
rotation_engrenages = 0


# ========== FONCTIONS HORLOGE ==========
def afficher_heure(tuple_heure):
    global heure_personnalisee
    heure_personnalisee = tuple_heure
    status_var.set("✓ Heure personnalisée activée")


def regler_alarme(tuple_heure):
    global alarme
    alarme = tuple_heure
    h, m, s = tuple_heure
    alarme_label.config(text=f"⏰ Alarme: {h:02d}:{m:02d}:{s:02d}")
    status_var.set("✓ Alarme configurée")


def incrementer_heure(h, m, s):
    s = s + 1
    if s >= 60:
        s = 0
        m = m + 1
    if m >= 60:
        m = 0
        h = h + 1
    if h >= 24:
        h = 0
    return (h, m, s)


def convertir_12h(heures, minutes, secondes):
    if heures == 0:
        heures_12 = 12
        periode = "AM"
    elif heures < 12:
        heures_12 = heures
        periode = "AM"
    elif heures == 12:
        heures_12 = 12
        periode = "PM"
    else:
        heures_12 = heures - 12
        periode = "PM"
    return heures_12, minutes, secondes, periode


def formater_affichage(heures, minutes, secondes):
    if mode_affichage == "12h":
        h12, m12, s12, periode = convertir_12h(heures, minutes, secondes)
        return f"{h12:02d}:{m12:02d}:{s12:02d}", periode
    else:
        return f"{heures:02d}:{minutes:02d}:{secondes:02d}", ""


def toggle_pause():
    global horloge_en_pause
    horloge_en_pause = not horloge_en_pause
    if horloge_en_pause:
        btn_pause.config(text="▶ REPRENDRE")
        status_var.set("⏸ Horloge en pause")
    else:
        btn_pause.config(text="⏸ PAUSE")
        status_var.set("✓ Horloge active")


def changer_mode():
    global mode_affichage
    if mode_affichage == "24h":
        mode_affichage = "12h"
        btn_mode.config(text="MODE 12H")
        status_var.set("✓ Mode 12H")
    else:
        mode_affichage = "24h"
        btn_mode.config(text="MODE 24H")
        status_var.set("✓ Mode 24H")


def ouvrir_config_heure():
    config = tk.Toplevel(root)
    config.title("⚙️ Configuration")
    config.geometry("420x400")
    config.configure(bg="#1a1a1a")
    config.resizable(False, False)
    
    tk.Label(
        config, text="⚙ RÉGLAGE HEURE ⚙",
        font=("Arial", 18, "bold"), fg="#d4a574", bg="#1a1a1a"
    ).pack(pady=20)
    
    frame = tk.Frame(config, bg="#1a1a1a")
    frame.pack(pady=20)
    
    tk.Label(frame, text="Heures (0-23)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=0, column=0, pady=10, padx=15, sticky="w")
    entry_h = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_h.grid(row=0, column=1, pady=10, padx=10)
    
    tk.Label(frame, text="Minutes (0-59)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=1, column=0, pady=10, padx=15, sticky="w")
    entry_m = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_m.grid(row=1, column=1, pady=10, padx=10)
    
    tk.Label(frame, text="Secondes (0-59)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=2, column=0, pady=10, padx=15, sticky="w")
    entry_s = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_s.grid(row=2, column=1, pady=10, padx=10)
    
    error_label = tk.Label(config, text="", font=("Arial", 10),
                          fg="#ff6666", bg="#1a1a1a")
    error_label.pack()
    
    def valider():
        try:
            h = int(entry_h.get())
            m = int(entry_m.get())
            s = int(entry_s.get())
            
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                error_label.config(text="❌ Valeurs invalides")
                return
            
            afficher_heure((h, m, s))
            config.destroy()
        except ValueError:
            error_label.config(text="❌ Entrez des nombres")
    
    tk.Button(
        config, text="✓ VALIDER", font=("Arial", 13, "bold"),
        bg="#8b6f47", fg="#000", width=15, height=2,
        command=valider, cursor="hand2"
    ).pack(pady=20)


def ouvrir_config_alarme():
    config = tk.Toplevel(root)
    config.title("⏰ Configuration")
    config.geometry("420x400")
    config.configure(bg="#1a1a1a")
    config.resizable(False, False)
    
    tk.Label(
        config, text="⏰ RÉGLAGE ALARME ⏰",
        font=("Arial", 18, "bold"), fg="#d4a574", bg="#1a1a1a"
    ).pack(pady=20)
    
    frame = tk.Frame(config, bg="#1a1a1a")
    frame.pack(pady=20)
    
    tk.Label(frame, text="Heures (0-23)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=0, column=0, pady=10, padx=15, sticky="w")
    entry_h = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_h.grid(row=0, column=1, pady=10, padx=10)
    
    tk.Label(frame, text="Minutes (0-59)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=1, column=0, pady=10, padx=15, sticky="w")
    entry_m = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_m.grid(row=1, column=1, pady=10, padx=10)
    
    tk.Label(frame, text="Secondes (0-59)", font=("Arial", 12),
             fg="#c9a66b", bg="#1a1a1a").grid(row=2, column=0, pady=10, padx=15, sticky="w")
    entry_s = tk.Entry(frame, font=("Arial", 14), width=8, justify="center",
                       bg="#2a2a2a", fg="#d4a574", insertbackground="#d4a574", bd=2)
    entry_s.grid(row=2, column=1, pady=10, padx=10)
    
    error_label = tk.Label(config, text="", font=("Arial", 10),
                          fg="#ff6666", bg="#1a1a1a")
    error_label.pack()
    
    def valider():
        try:
            h = int(entry_h.get())
            m = int(entry_m.get())
            s = int(entry_s.get())
            
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                error_label.config(text="❌ Valeurs invalides")
                return
            
            regler_alarme((h, m, s))
            config.destroy()
        except ValueError:
            error_label.config(text="❌ Entrez des nombres")
    
    tk.Button(
        config, text="✓ VALIDER", font=("Arial", 13, "bold"),
        bg="#8b6f47", fg="#000", width=15, height=2,
        command=valider, cursor="hand2"
    ).pack(pady=20)


def desactiver_alarme():
    global alarme
    alarme = None
    alarme_label.config(text="⏰ Aucune alarme")
    status_var.set("✓ Alarme désactivée")


def alarme_popup():
    global alarme_active
    if alarme_active:
        return
    
    alarme_active = True
    popup = tk.Toplevel(root)
    popup.title("⏰ ALARME")
    popup.geometry("500x300")
    popup.configure(bg="#1a1a1a")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()
    
    tk.Label(
        popup,
        text="⚙ ALARME ⚙",
        font=("Arial", 32, "bold"),
        fg="#d4a574",
        bg="#1a1a1a"
    ).pack(pady=30)
    
    tk.Label(
        popup,
        text="Il est temps\nMamie Jeannine !",
        font=("Arial", 20, "bold"),
        fg="#c9a66b",
        bg="#1a1a1a"
    ).pack(pady=20)
    
    def fermer():
        global alarme_active
        alarme_active = False
        popup.destroy()
        desactiver_alarme()
    
    tk.Button(
        popup,
        text="✓ ARRÊTER",
        font=("Arial", 16, "bold"),
        bg="#8b6f47",
        fg="#000",
        command=fermer,
        width=18,
        height=2,
        cursor="hand2"
    ).pack(pady=30)


def dessiner_engrenage(x, y, rayon, dents, rotation, couleur_base, couleur_dent):
    """Dessine un engrenage détaillé"""
    # Cercle de base
    canvas.create_oval(
        x - rayon, y - rayon,
        x + rayon, y + rayon,
        fill=couleur_base, outline="#3d2817", width=2
    )
    
    # Dents de l'engrenage
    for i in range(dents):
        angle1 = math.radians(i * (360 / dents) + rotation)
        angle2 = math.radians((i + 0.4) * (360 / dents) + rotation)
        angle3 = math.radians((i + 0.6) * (360 / dents) + rotation)
        angle4 = math.radians((i + 1) * (360 / dents) + rotation)
        
        # Points de la dent
        x1 = x + rayon * math.cos(angle1)
        y1 = y + rayon * math.sin(angle1)
        x2 = x + (rayon + 8) * math.cos(angle2)
        y2 = y + (rayon + 8) * math.sin(angle2)
        x3 = x + (rayon + 8) * math.cos(angle3)
        y3 = y + (rayon + 8) * math.sin(angle3)
        x4 = x + rayon * math.cos(angle4)
        y4 = y + rayon * math.sin(angle4)
        
        canvas.create_polygon(
            x1, y1, x2, y2, x3, y3, x4, y4,
            fill=couleur_dent, outline="#3d2817", width=1
        )
    
    # Cercle intérieur plus sombre
    rayon_int = rayon * 0.6
    canvas.create_oval(
        x - rayon_int, y - rayon_int,
        x + rayon_int, y + rayon_int,
        fill="#2d1f15", outline="#1a0f08", width=2
    )
    
    # Vis centrale
    canvas.create_oval(x - 6, y - 6, x + 6, y + 6,
                      fill="#4a3420", outline="#2d1810", width=2)
    canvas.create_line(x - 4, y, x + 4, y, fill="#1a0f08", width=1)
    canvas.create_line(x, y - 4, x, y + 4, fill="#1a0f08", width=1)


# ========== ANIMATION PRINCIPALE ==========
def animer_horloge():
    global heure_personnalisee, rotation_engrenages
    
    canvas.delete("all")
    
    # Fond noir pur comme l'image
    canvas.create_rectangle(0, 0, 900, 750, fill="#0d0d0d", outline="")
    
    # Obtenir l'heure
    if not horloge_en_pause:
        if heure_personnalisee is not None:
            heures, minutes, secondes = heure_personnalisee
            heure_personnalisee = incrementer_heure(heures, minutes, secondes)
        else:
            maintenant = datetime.now()
            heures = maintenant.hour
            minutes = maintenant.minute
            secondes = maintenant.second
        
        rotation_engrenages += 1
        
        # Vérifier alarme
        if alarme is not None and not alarme_active:
            if (heures, minutes, secondes) == alarme:
                alarme_popup()
    else:
        heures, minutes, secondes = heure_personnalisee if heure_personnalisee else (0, 0, 0)
    
    # ===== CERCLE EXTÉRIEUR GRIS FONCÉ =====
    canvas.create_oval(200, 120, 700, 620, fill="#3d3d3d", outline="#2a2a2a", width=8)
    
    # ===== FOND NOIR DE L'HORLOGE =====
    canvas.create_oval(220, 140, 680, 600, fill="#0d0d0d", outline="", width=0)
    
    # ===== CHIFFRES DORÉS STYLE IMAGE =====
    chiffres = ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        x_num = 450 + 165 * math.cos(angle)
        y_num = 370 + 165 * math.sin(angle)
        
        # Chiffre doré comme l'image
        canvas.create_text(x_num, y_num, text=chiffres[i],
                          fill="#d4a574", font=("Georgia", 28, "bold"))
    
    # ===== PETITS POINTS MINUTES =====
    for i in range(60):
        if i % 5 != 0:
            angle = math.radians(i * 6 - 90)
            x1 = 450 + 145 * math.cos(angle)
            y1 = 370 + 145 * math.sin(angle)
            canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill="#8b6f47", outline="")
    
    # ===== ENGRENAGES VISIBLES AU CENTRE =====
    centre_x, centre_y = 450, 370
    
    # Grand engrenage central doré (comme dans l'image)
    dessiner_engrenage(centre_x, centre_y, 70, 16, rotation_engrenages * 0.3,
                      "#8b6f47", "#a68555")
    
    # Petits engrenages autour
    positions = [
        (centre_x - 80, centre_y - 80, 35, 12, -rotation_engrenages * 0.8),
        (centre_x + 80, centre_y - 80, 30, 10, rotation_engrenages * 1.2),
        (centre_x - 85, centre_y + 75, 32, 11, rotation_engrenages * 0.9),
        (centre_x + 85, centre_y + 80, 28, 9, -rotation_engrenages * 1.1),
    ]
    
    for px, py, pr, pd, rot in positions:
        dessiner_engrenage(px, py, pr, pd, rot, "#7a5f3d", "#8b6f47")
    
    # ===== AIGUILLES STYLE INDUSTRIEL =====
    # Aiguille des heures (large et dorée)
    angle_h = math.radians((heures % 12) * 30 + minutes * 0.5 - 90)
    x_h = centre_x + 85 * math.cos(angle_h)
    y_h = centre_y + 85 * math.sin(angle_h)
    
    # Forme aiguille épaisse
    canvas.create_line(centre_x, centre_y, x_h, y_h,
                      fill="#5c4a2e", width=16, capstyle=tk.ROUND)
    canvas.create_line(centre_x, centre_y, x_h, y_h,
                      fill="#8b6f47", width=12, capstyle=tk.ROUND)
    canvas.create_line(centre_x, centre_y, x_h, y_h,
                      fill="#a68555", width=8, capstyle=tk.ROUND)
    
    # Aiguille des minutes (moyenne)
    angle_m = math.radians(minutes * 6 - 90)
    x_m = centre_x + 120 * math.cos(angle_m)
    y_m = centre_y + 120 * math.sin(angle_m)
    
    canvas.create_line(centre_x, centre_y, x_m, y_m,
                      fill="#5c4a2e", width=14, capstyle=tk.ROUND)
    canvas.create_line(centre_x, centre_y, x_m, y_m,
                      fill="#8b6f47", width=10, capstyle=tk.ROUND)
    canvas.create_line(centre_x, centre_y, x_m, y_m,
                      fill="#c9a66b", width=6, capstyle=tk.ROUND)
    
    # Aiguille des secondes (fine et cuivre)
    angle_s = math.radians(secondes * 6 - 90)
    x_s = centre_x + 140 * math.cos(angle_s)
    y_s = centre_y + 140 * math.sin(angle_s)
    
    canvas.create_line(centre_x, centre_y, x_s, y_s,
                      fill="#b87333", width=4, capstyle=tk.ROUND)
    
    # Centre avec vis visible
    canvas.create_oval(centre_x - 15, centre_y - 15,
                      centre_x + 15, centre_y + 15,
                      fill="#4a3420", outline="#2d1810", width=3)
    canvas.create_oval(centre_x - 8, centre_y - 8,
                      centre_x + 8, centre_y + 8,
                      fill="#8b6f47", outline="")
    
    # Croix sur vis
    canvas.create_line(centre_x - 6, centre_y, centre_x + 6, centre_y,
                      fill="#1a0f08", width=2)
    canvas.create_line(centre_x, centre_y - 6, centre_x, centre_y + 6,
                      fill="#1a0f08", width=2)
    
    # ===== AFFICHAGE DIGITAL EN BAS =====
    texte_heure, periode = formater_affichage(heures, minutes, secondes)
    
    # Fond pour le digital
    canvas.create_rectangle(340, 640, 560, 690, fill="#1a1a1a", outline="#8b6f47", width=3)
    
    canvas.create_text(450, 665, text=texte_heure,
                      font=("Arial", 28, "bold"), fill="#d4a574")
    
    if periode:
        canvas.create_text(530, 665, text=periode,
                          font=("Arial", 16, "bold"), fill="#c9a66b")
    
    # Status pause
    if horloge_en_pause:
        canvas.create_rectangle(370, 50, 530, 95, fill="#1a1a1a",
                               outline="#8b6f47", width=3)
        canvas.create_text(450, 72, text="⏸ PAUSE",
                          font=("Arial", 18, "bold"), fill="#d4a574")
    
    root.after(40, animer_horloge)


# ========== INTERFACE PRINCIPALE ==========
root = tk.Tk()
root.title("⚙️ Horloge Steampunk Mécanique")
root.geometry("900x820")
root.configure(bg="#0d0d0d")
root.resizable(False, False)

# ===== CANVAS =====
canvas = tk.Canvas(root, width=900, height=750, bg="#0d0d0d", highlightthickness=0)
canvas.pack()

# ===== CONTRÔLES =====
control_panel = tk.Frame(root, bg="#0d0d0d")
control_panel.pack(fill="x")

btn_frame = tk.Frame(control_panel, bg="#0d0d0d")
btn_frame.pack(pady=8)

btn_pause = tk.Button(
    btn_frame,
    text="⏸ PAUSE",
    font=("Arial", 11, "bold"),
    bg="#8b6f47",
    fg="#000",
    width=11,
    height=2,
    command=toggle_pause,
    cursor="hand2"
)
btn_pause.grid(row=0, column=0, padx=8)

btn_mode = tk.Button(
    btn_frame,
    text="MODE 24H",
    font=("Arial", 11, "bold"),
    bg="#8b6f47",
    fg="#000",
    width=11,
    height=2,
    command=changer_mode,
    cursor="hand2"
)
btn_mode.grid(row=0, column=1, padx=8)

btn_heure = tk.Button(
    btn_frame,
    text="⚙ RÉGLER HEURE",
    font=("Arial", 10, "bold"),
    bg="#a68555",
    fg="#000",
    width=14,
    height=2,
    command=ouvrir_config_heure,
    cursor="hand2"
)
btn_heure.grid(row=0, column=2, padx=8)

btn_alarme = tk.Button(
    btn_frame,
    text="⏰ RÉGLER ALARME",
    font=("Arial", 10, "bold"),
    bg="#a68555",
    fg="#000",
    width=14,
    height=2,
    command=ouvrir_config_alarme,
    cursor="hand2"
)
btn_alarme.grid(row=0, column=3, padx=8)

# ===== FOOTER =====
footer = tk.Frame(root, bg="#0d0d0d")
footer.pack(fill="x")

status_var = tk.StringVar(value="✓ Horloge active")
status_label = tk.Label(
    footer,
    textvariable=status_var,
    font=("Arial", 10),
    fg="#d4a574",
    bg="#0d0d0d"
)
status_label.pack(side="left", padx=20, pady=4)

alarme_label = tk.Label(
    footer,
    text="⏰ Aucune alarme",
    font=("Arial", 10),
    fg="#c9a66b",
    bg="#0d0d0d"
)
alarme_label.pack(side="left", padx=18, pady=4)

signature = tk.Label(
    footer,
    text="⚙ Pour Mamie Jeannine ⚙",
    font=("Arial", 9, "italic"),
    fg="#8b6f47",
    bg="#0d0d0d"
)
signature.pack(side="right", padx=20, pady=4)

animer_horloge()
root.mainloop()