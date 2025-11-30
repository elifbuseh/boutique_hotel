import customtkinter as ctk

# Tema: LIGHT + modern
APPEARANCE_MODE = "light"
# Default temayı "blue" olarak bırakıyoruz, ancak COLORS ile override ediyoruz.
DEFAULT_COLOR_THEME = "blue"

# Font yolları (Dosya yapınızdaki Poppins klasörünü varsayar)
FONT_FILES = [
    "Poppins/Poppins-Regular.ttf",
    "Poppins/Poppins-Medium.ttf",
    "Poppins/Poppins-Bold.ttf",
]

# Uygulama genelinde kullanacağımız font setleri
FONT_SETS = {
    "header": ("Poppins", 26, "bold"),
    "sidebar": ("Poppins", 14, "bold"),
    "title": ("Poppins", 20, "bold"),
    "subtitle": ("Poppins", 13),
    "card_type": ("Poppins", 12),
    "card_number": ("Poppins", 26, "bold"),
    "badge": ("Poppins", 11, "bold"),
    "floor": ("Poppins", 18, "bold"),
    "normal": ("Poppins", 12),
}

# --- GUNCEL RENKLER (CSS Estetiğine Benzerlik İçin) ---
COLORS = {
    # Web'deki hafif gri/beyaz arka planı taklit etmek için daha nötr, çok hafif mavi/gri.
    "bg": "#f8fafd",        # Ana arka plan (Web'deki gibi temiz)
    "panel": "#ffffff",     # İçerik paneli / Kart zemini
    "card": "#ffffff",      # Kart zemini (Temiz beyaz)

    # CSS'teki #646cffaa mor/mavi tonunu sidebar için kullanıyoruz.
    "sidebar": "#000b5c",       # Sidebar / Üst bar (Modern Mavi/Mor)
    "sidebar_dark": "#000319",  # Sidebar hover (Daha koyu tonu)
    "sidebar_light": "#e0e3ff", # Aktif nav vurgu (Çok açık mavi, beyaz metin kontrastı için)

    "accent": "#000b5c",    # Ana vurgu (Butonlar) - Sidebar rengiyle eşleşmeli
    "accent_alt": "#ffdd94", # İkincil vurguyu sarı bırakıyoruz.
    
    "text_main": "#1f2430", # Koyu metin
}


def apply_appearance():
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(DEFAULT_COLOR_THEME)


def load_fonts():
    for font_file in FONT_FILES:
        try:
            ctk.FontManager.load_font(font_file)
        except Exception:
            # Font yüklenemezse default'a düşsün
            pass