# login.py

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import threading 

# backend.services' modülünün projenizde mevcut olduğunu varsayıyoruz (app.py'de kullanılıyor)
# import backend.services.hotel_service as db 

# --- RENKLER VE FONTLAR (CSS'e uygun) ---
CTK_COLORS = {
    # CSS: background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    "BG_GRADIENT_START": "#0f2027", 
    "BG_GRADIENT_END": "#2c5364",
    
    # CSS: .login-brand, .forgot-password-link, .remember-me input:focus
    "ACCENT_BLUE_DARK": "#1e3c72", 
    "ACCENT_BLUE_HOVER": "#2a5298",

    # CSS: .login-container
    "CARD_BG": "#ffffff",
    "INPUT_BORDER": "#eee",
    "INPUT_BG": "#fdfdfd",
    "TEXT_DARK": "#333",
    "TEXT_SUBTLE": "#888",
}

# --- FONT SETLERİ ---
FONT_FAMILY = "Segoe UI"
LOGIN_FONTS = {
    "brand": (FONT_FAMILY, 28, "bold"),
    "subtitle": (FONT_FAMILY, 14),
    "title": (FONT_FAMILY, 22, "bold"),
    "input": (FONT_FAMILY, 15),
    "button": (FONT_FAMILY, 16, "bold"),
    "options": (FONT_FAMILY, 14),
}


class LoginApp(ctk.CTk):
    # on_login_success_callback: Giriş başarılı olduğunda ana uygulamayı başlatacak fonksiyon
    def __init__(self, on_login_success_callback=None): 
        super().__init__()
        
        # Tema Ayarları
        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue") 
        
        self.title("BS HOTEL - Yönetim Paneli")
        self.geometry("800x600")
        self.min_width = 700
        self.min_height = 500
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.is_loading = False
        self.show_password_state = False
        self.on_login_success_callback = on_login_success_callback

        # --- Arka Plan Çerçevesi (CSS .login-bg) ---
        self.login_bg = ctk.CTkFrame(
            self, 
            fg_color=CTK_COLORS["BG_GRADIENT_END"], 
            corner_radius=0
        )
        self.login_bg.grid(row=0, column=0, sticky="nsew")
        self.login_bg.grid_rowconfigure(0, weight=1)
        self.login_bg.grid_columnconfigure(0, weight=1)
        
        # --- Giriş Kartı (CSS .login-container) ---
        self.login_card = ctk.CTkFrame(
            self.login_bg,
            fg_color=CTK_COLORS["CARD_BG"],
            corner_radius=24
        )
        self.login_card.grid(row=0, column=0, padx=20, pady=20)
        self.login_card.grid_columnconfigure(0, weight=1)
        
        self.create_login_widgets()

    def create_login_widgets(self):
        
        # Üst Şerit simülasyonu (Header)
        header_strip = ctk.CTkFrame(
            self.login_card,
            fg_color=CTK_COLORS["ACCENT_BLUE_DARK"],
            height=6,
            corner_radius=0
        )
        header_strip.grid(row=0, column=0, sticky="new", padx=-24, pady=(0, 0))

        # Başlıklar
        ctk.CTkLabel(
            self.login_card,
            text="BS HOTEL",
            font=ctk.CTkFont(*LOGIN_FONTS["brand"]),
            text_color=CTK_COLORS["ACCENT_BLUE_DARK"]
        ).grid(row=1, column=0, padx=40, pady=(39, 0), sticky="s")
        
        ctk.CTkLabel(
            self.login_card,
            text="Yönetim Paneli",
            font=ctk.CTkFont(*LOGIN_FONTS["subtitle"]),
            text_color=CTK_COLORS["TEXT_SUBTLE"]
        ).grid(row=2, column=0, padx=40, pady=(0, 20), sticky="n")

        ctk.CTkLabel(
            self.login_card,
            text="Hoş Geldiniz",
            font=ctk.CTkFont(*LOGIN_FONTS["title"]),
            text_color=CTK_COLORS["TEXT_DARK"]
        ).grid(row=3, column=0, padx=40, pady=(0, 25))

        # --- Form Alanı ---
        form_frame = ctk.CTkFrame(self.login_card, fg_color="transparent")
        form_frame.grid(row=4, column=0, padx=40, sticky="ew")
        form_frame.grid_columnconfigure(0, weight=1)

        # Kullanıcı Adı
        self.username_entry = self.create_input(form_frame, 0, "Kullanıcı Adı")
        self.password_entry = self.create_input(form_frame, 1, "Şifre", is_password=True)

        # Şifre Gösterme Butonu
        self.password_toggle_button = ctk.CTkButton(
            form_frame,
            text="🐵",
            width=20,
            height=20,
            fg_color="transparent",
            text_color=CTK_COLORS["TEXT_DARK"],
            hover_color=CTK_COLORS["ACCENT_BLUE_HOVER"],
            command=self.toggle_password,
            font=ctk.CTkFont(size=18)
        )
        
        # Şifre giriş alanının boyutlandırma ve yerleştirme olaylarını dinle
        def on_password_entry_config(event):
            # Butonun, şifre giriş alanının tam sağ kenarına ve dikey ortasına yerleştirilmesi
            if self.password_entry.winfo_height() > 0:
                self.password_toggle_button.place(
                    relx=1.0, 
                    # Hesaplama: Widget'ın başlangıç Y konumu + yarısı + üst/alt boşluk telafisi (pady=10)
                    rely=self.password_entry.winfo_y() + self.password_entry.winfo_height() / 2 + 10, 
                    anchor="e", 
                    x=-16
                )
        
        # Password entry'nin boyutları belirlendikten sonra konumu ayarlama
        self.password_entry.bind("<Configure>", on_password_entry_config)

        # Seçenekler (Beni Hatırla & Şifremi Unuttum)
        options_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 30))
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)

        # Beni Hatırla
        self.remember_me_check = ctk.CTkCheckBox(
            options_frame,
            text="Beni Hatırla",
            font=ctk.CTkFont(*LOGIN_FONTS["options"]),
            text_color=CTK_COLORS["TEXT_DARK"],
            fg_color=CTK_COLORS["ACCENT_BLUE_DARK"],
            hover_color=CTK_COLORS["ACCENT_BLUE_HOVER"]
        )
        self.remember_me_check.grid(row=0, column=0, sticky="w")
        
        # Şifremi Unuttum (Link simülasyonu)
        ctk.CTkLabel(
            options_frame,
            text="Şifremi Unuttum?",
            font=ctk.CTkFont(*LOGIN_FONTS["options"], underline=True),
            text_color=CTK_COLORS["ACCENT_BLUE_DARK"],
            cursor="hand2"
        ).grid(row=0, column=1, sticky="e")
        
        # Giriş Butonu
        self.login_button = ctk.CTkButton(
            form_frame,
            text="GİRİŞ YAP",
            font=ctk.CTkFont(*LOGIN_FONTS["button"]),
            fg_color=CTK_COLORS["ACCENT_BLUE_DARK"],
            hover_color="#162d55", # CSS hover rengi
            text_color="white",
            height=50,
            corner_radius=12,
            command=self.start_login_thread
        )
        self.login_button.grid(row=3, column=0, sticky="ew", pady=(0, 45))
        
    def create_input(self, parent, row, placeholder, is_password=False):
        """CSS'teki .login-input stilini taklit eden giriş alanı oluşturur."""
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            show="*" if is_password and not self.show_password_state else "",
            font=ctk.CTkFont(*LOGIN_FONTS["input"]),
            text_color=CTK_COLORS["TEXT_DARK"],
            fg_color=CTK_COLORS["INPUT_BG"],
            border_color=CTK_COLORS["INPUT_BORDER"],
            border_width=2,
            height=45,
            corner_radius=12
        )
        entry.grid(row=row, column=0, sticky="ew", pady=10)
        return entry

    def toggle_password(self):
        """Şifre göster/gizle işlevini yönetir."""
        self.show_password_state = not self.show_password_state
        if self.show_password_state:
            self.password_entry.configure(show="")
            self.password_toggle_button.configure(text="🙈")
        else:
            self.password_entry.configure(show="*")
            self.password_toggle_button.configure(text="🐵")

    def start_login_thread(self):
        """Giriş işlemini donmayı önlemek için ayrı bir thread'de başlatır."""
        if not self.is_loading:
            self.is_loading = True
            self.update_loading_state()
            # Threading'i kullanarak simüle edilmiş API çağrısını başlat
            login_thread = threading.Thread(target=self.handle_login_simulation)
            login_thread.start()

    def update_loading_state(self):
        """Loading durumuna göre buton görünümünü günceller."""
        if self.is_loading:
            self.login_button.configure(text="Giriş Yapılıyor...", state="disabled")
        else:
            self.login_button.configure(text="GİRİŞ YAP", state="normal")

    def handle_login_simulation(self):
        """
        Giriş işlemini simüle eder.
        Gerçek uygulamada burası db.login(username, password) çağrısı olur.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Simüle edilmiş API gecikmesi
        time.sleep(1.5) 
        
        # Başarılı giriş için: admin/123
        success = (username == "admin" and password == "123")
        
        # Ana thread'e geri dönerek UI'ı güncelle
        self.after(0, lambda: self.finish_login_attempt(success, username))

    def finish_login_attempt(self, success, username):
        """Giriş denemesi sonucunda UI'ı günceller."""
        self.is_loading = False
        self.update_loading_state()
        
        if success:
            messagebox.showinfo("Başarılı", f"Hoş geldiniz, {username}! Giriş başarılı.")
            self.destroy() # Login penceresini kapat
            if self.on_login_success_callback:
                self.on_login_success_callback() # Callback'i çağırarak ana uygulamayı başlat
        else:
            messagebox.showerror("Hata", "Giriş başarısız! Lütfen bilgilerinizi kontrol edin.")

# login.py dosyasının sonunda başka bir kod bulunmamalıdır.