import customtkinter as ctk
from tkinter import messagebox
from backend.services import hotel_service as db

# --- YARDIMCI FONSİYON: Formu Temizleme ---

def clear_room_type_form(app):
    """Formu temizler ve Ekle moduna geri döner."""
    app.selected_room_type_id = None
    app.entry_rt_name.delete(0, "end")
    app.entry_rt_desc.delete(0, "end")
    app.entry_rt_price.delete(0, "end")
    app.entry_rt_capacity.delete(0, "end")
    
    app.label_rt_message.configure(text="", text_color="#6b7280")
    # Ekle/Kaydet butonu Ant Design Primary Blue olarak ayarlandı
    app.btn_rt_save.configure(
        text="Ekle", 
        fg_color="#1890ff", 
        hover_color="#096dd9",
        text_color="white"
    )

# --- ANA FRAME VE LİSTE FONKSİYONLARI ---

def create_room_types_frame(app, parent):
    """Oda Tipleri Yönetimi Ana Frame'ini oluşturur (Ant Design Card stili)."""
    
    # Ant Design Card görünümü
    frame = ctk.CTkFrame(parent, corner_radius=24, fg_color=app.color_card, bg_color=app.color_bg) 

    # --- BAŞLIK VE AÇIKLAMA ---
    title = ctk.CTkLabel(
        frame,
        text="Oda Tipleri & Fiyatlandırma",
        font=app.font_title,
        text_color="#111827"
    )
    title.pack(pady=(25, 4), anchor="w", padx=25)

    subtitle = ctk.CTkLabel(
        frame,
        text="Oda tiplerinin adını, açıklamasını, taban fiyatını ve kapasitesini yönetebilirsiniz.",
        font=app.font_subtitle,
        text_color="#6b7280"
    )
    subtitle.pack(pady=(0, 15), anchor="w", padx=25)

    # --- YENİ TİP EKLE / GÜNCELLE FORMU (Grid Tabanlı) ---
    form_frame = ctk.CTkFrame(frame, corner_radius=16, fg_color=app.color_panel)
    form_frame.pack(fill="x", padx=20, pady=(5, 10))
    
    # Grid yapılandırması
    for i in range(6):
        form_frame.grid_columnconfigure(i, weight=1 if i in (1, 3, 5) else 0)

    # Tip Adı
    lbl_name = ctk.CTkLabel(form_frame, text="Tip Adı:", font=app.font_normal, text_color="#111827")
    lbl_name.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")
    app.entry_rt_name = ctk.CTkEntry(form_frame, font=app.font_normal, placeholder_text="Standart Oda")
    app.entry_rt_name.grid(row=0, column=1, padx=(0, 15), pady=10, sticky="ew")

    # Taban Fiyat
    lbl_price = ctk.CTkLabel(form_frame, text="Taban Fiyat:", font=app.font_normal, text_color="#111827")
    lbl_price.grid(row=0, column=2, padx=(15, 5), pady=10, sticky="w")
    app.entry_rt_price = ctk.CTkEntry(form_frame, font=app.font_normal, placeholder_text="1500 (₺)")
    app.entry_rt_price.grid(row=0, column=3, padx=(0, 15), pady=10, sticky="ew")

    # Kapasite
    lbl_cap = ctk.CTkLabel(form_frame, text="Kapasite:", font=app.font_normal, text_color="#111827")
    lbl_cap.grid(row=0, column=4, padx=(15, 5), pady=10, sticky="w")
    app.entry_rt_capacity = ctk.CTkEntry(form_frame, font=app.font_normal, placeholder_text="2")
    app.entry_rt_capacity.grid(row=0, column=5, padx=(0, 15), pady=10, sticky="ew")

    # Açıklama (Tüm satırı kaplar)
    lbl_desc = ctk.CTkLabel(form_frame, text="Açıklama:", font=app.font_normal, text_color="#111827")
    lbl_desc.grid(row=1, column=0, padx=(15, 5), pady=4, sticky="w")
    app.entry_rt_desc = ctk.CTkEntry(form_frame, font=app.font_normal, placeholder_text="Oda tipi hakkında kısa açıklama")
    app.entry_rt_desc.grid(row=1, column=1, columnspan=5, padx=(0, 15), pady=4, sticky="ew")
    
    # Mesaj Alanı
    app.label_rt_message = ctk.CTkLabel(form_frame, text="", font=("Poppins", 11), text_color="#6b7280")
    app.label_rt_message.grid(row=2, column=0, columnspan=4, padx=15, pady=(8, 15), sticky="w")

    # Aksiyon Butonları (Sağ Alt Köşe)
    action_buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    action_buttons_frame.grid(row=2, column=4, columnspan=2, padx=15, pady=(8, 15), sticky="e")
    
    # Sil Butonu (React danger/Red)
    app.btn_rt_delete = ctk.CTkButton(
        action_buttons_frame, 
        text="Sil", 
        font=app.font_normal,
        fg_color="#ff4d4f", # Ant Design Red
        hover_color="#cf1322",
        text_color="white",
        command=lambda: delete_room_type(app),
        corner_radius=8,
        width=80
    )
    app.btn_rt_delete.pack(side="left", padx=(10, 5)) 
    
    # Ekle/Güncelle Butonu (React Primary/Blue - başlangıçta Ekle)
    app.btn_rt_save = ctk.CTkButton(
        action_buttons_frame, 
        text="Ekle", 
        font=app.font_normal,
        fg_color="#1890ff", # Ant Design Primary Blue
        hover_color="#096dd9",
        text_color="white",
        command=lambda: save_room_type(app),
        corner_radius=8,
        width=100
    )
    app.btn_rt_save.pack(side="left")

    # --- ODA TİPLERİ LİSTESİ (Ant Design Table Taklidi) ---
    app.room_types_scroll = ctk.CTkScrollableFrame(
        frame, corner_radius=16, width=900, height=400, fg_color=app.color_panel
    )
    app.room_types_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 25))

    build_room_type_list(app)
    return frame

def build_room_type_list(app):
    """Oda tipi listesini Ant Design Table stiliyle oluşturur."""
    for child in app.room_types_scroll.winfo_children():
        child.destroy()

    try:
        room_types = db.get_all_room_types()
    except Exception as e:
        messagebox.showerror("DB Hatası", f"Oda tipleri yüklenirken hata: {e}")
        room_types = []
        
    if not room_types:
        lbl = ctk.CTkLabel(
            app.room_types_scroll,
            text="Tanımlı oda tipi yok.",
            font=app.font_normal,
            text_color="#111827"
        )
        lbl.pack(pady=20)
        return

    # --- TABLO BAŞLIĞI (HEADER) ---
    # Açık gri başlık rengi (#f0f2f5)
    header = ctk.CTkFrame(app.room_types_scroll, fg_color="#f0f2f5", corner_radius=12) 
    header.pack(fill="x", padx=10, pady=(8, 4))

    cols = ["ID", "Tip Adı", "Açıklama", "Taban Fiyat", "Kapasite", "İşlemler"]
    widths = [40, 150, 240, 100, 80, 120] 

    for i, (col, w) in enumerate(zip(cols, widths)):
        lbl = ctk.CTkLabel(
            header,
            text=col,
            font=("Poppins", 11, "bold"),
            text_color="#595959", 
            width=w,
            anchor="w" if i != len(cols) - 1 else "center"
        )
        lbl.grid(row=0, column=i, padx=(8 if i == 0 else 5, 5), pady=8, sticky="w" if i != len(cols) - 1 else "e") 

    # --- TABLO SATIRLARI ---
    for row_idx, rt in enumerate(room_types):
        rt_id, name, desc, price, cap = rt
        
        # Satır arkaplanı: Beyaz ve çok açık gri (#fbfbfb)
        bg_color = "#ffffff" if row_idx % 2 == 0 else "#fbfbfb" 
        row = ctk.CTkFrame(app.room_types_scroll, fg_color=bg_color, corner_radius=12)
        row.pack(fill="x", padx=10, pady=3)

        values = [
            str(rt_id),
            name or "-",
            desc or "-",
            f"{price:.2f} ₺" if price is not None else "-",
            f"{cap} Kişilik" if cap is not None else "-"
        ]

        for i, (val, w) in enumerate(zip(values, widths[:-1])):
            font = app.font_normal
            text_color = "#111827"
            fg_color = "transparent"

            if i == 1: # Tip Adı (Daha koyu ve kalın)
                text_color = "#1e3c72"
                font = ("Poppins", 12, "bold")
            elif i == 3: # Fiyat (Ant Design Gold Tag)
                text_color = "#d4b106"
                fg_color = "#fffbe6"
                font = ("Poppins", 11, "bold")
            elif i == 4: # Kapasite (Ant Design Purple Tag)
                text_color = "#531dab"
                fg_color = "#f9f0ff"
                font = ("Poppins", 11, "bold")

            lbl = ctk.CTkLabel(
                row,
                text=val,
                font=font,
                text_color=text_color,
                fg_color=fg_color,
                corner_radius=8,
                width=w,
                anchor="w",
                padx=8, 
                pady=6
            )
            lbl.grid(row=0, column=i, padx=(5 if i != 0 else 8, 5), pady=4, sticky="w") 

        # --- İŞLEMLER BUTONU ---
        # Düzenle Butonu (React'teki mavi hafif buton)
        btn_edit = ctk.CTkButton(
            row,
            text="Düzenle",
            width=80,
            font=("Poppins", 10, "bold"),
            fg_color="#e6f7ff", # Açık Mavi
            hover_color="#bae7ff",
            text_color="#1890ff",
            border_color="#91d5ff",
            border_width=1,
            corner_radius=10, 
            command=lambda rid=rt_id, n=name, d=desc, p=price, c=cap:
                load_room_type_into_form(app, rid, n, d, p, c)
        )
        btn_edit.grid(row=0, column=len(values), padx=8, pady=4, sticky="e")


def load_room_type_into_form(app, rt_id, name, desc, price, cap):
    """Seçilen oda tipi verilerini forma yükler ve Güncelle moduna geçirir (Ant Design Warning/Orange)."""
    app.selected_room_type_id = rt_id
    
    # Formu temizle ve doldur
    app.entry_rt_name.delete(0, "end")
    app.entry_rt_name.insert(0, name or "")
    app.entry_rt_desc.delete(0, "end")
    app.entry_rt_desc.insert(0, desc or "")
    app.entry_rt_price.delete(0, "end")
    if price is not None:
        # Fiyatı sadece sayı olarak yükle
        app.entry_rt_price.insert(0, str(price)) 
    app.entry_rt_capacity.delete(0, "end")
    if cap is not None:
        app.entry_rt_capacity.insert(0, str(cap))
        
    # Buton metnini ve rengini Güncelle olarak ayarla (Ant Design Warning Orange)
    app.label_rt_message.configure(
        text=f"Oda tipi düzenleniyor (ID={rt_id}).",
        text_color="#faad14" 
    )
    app.btn_rt_save.configure(
        text="Güncelle",
        fg_color="#faad14", 
        hover_color="#d48806",
        text_color="white"
    )


def save_room_type(app):
    """Oda tipini ekler veya günceller."""
    name = app.entry_rt_name.get().strip()
    desc = app.entry_rt_desc.get().strip() or None
    price_str = app.entry_rt_price.get().strip()
    cap_str = app.entry_rt_capacity.get().strip()

    if not name or not price_str or not cap_str:
        app.label_rt_message.configure(text="Tip adı, fiyat ve kapasite zorunludur.", text_color="#dc2626")
        return

    try:
        price = float(price_str)
        cap = int(cap_str)
        if price < 0 or cap < 1:
             app.label_rt_message.configure(text="Fiyat sıfırdan küçük, kapasite birden küçük olamaz.", text_color="#dc2626")
             return
    except ValueError:
        app.label_rt_message.configure(text="Fiyat ve kapasite sayısal olmalıdır.", text_color="#dc2626")
        return

    try:
        if app.selected_room_type_id is None:
            # EKLEME
            new_id = db.insert_room_type(name, desc, price, cap)
            if new_id is not None:
                app.label_rt_message.configure(
                    text=f"✅ Oda tipi başarıyla eklendi (ID={new_id}).",
                    text_color="#16a34a" # Ant Design Success Color
                )
            else:
                raise Exception("DB Ekleme Başarısız")
        else:
            # GÜNCELLEME
            ok = db.update_room_type(app.selected_room_type_id, name, desc, price, cap)
            if ok:
                app.label_rt_message.configure(
                    text=f"✅ Oda tipi başarıyla güncellendi (ID={app.selected_room_type_id}).",
                    text_color="#16a34a"
                )
            else:
                raise Exception("DB Güncelleme Başarısız")
                
        # Başarılı işlem sonrası temizleme ve yenileme
        clear_room_type_form(app)
        build_room_type_list(app)
        if hasattr(app, 'build_room_cards'): app.build_room_cards()

    except Exception as e:
        error_msg = f"❌ İşlem başarısız: {e}"
        app.label_rt_message.configure(text=error_msg, text_color="#dc2626")


def delete_room_type(app):
    """Seçili oda tipini siler."""
    if app.selected_room_type_id is None:
        app.label_rt_message.configure(
            text="Silmek için önce listeden bir oda tipi seçin.",
            text_color="#dc2626"
        )
        return

    # Silme onayı (Popconfirm taklidi)
    if not messagebox.askyesno(
        "Silme Onayı", 
        f"ID {app.selected_room_type_id} numaralı oda tipini silmek istediğinizden emin misiniz?"
    ):
        return

    try:
        ok = db.delete_room_type(app.selected_room_type_id)
        if ok:
            app.label_rt_message.configure(
                text=f"✅ Oda tipi başarıyla silindi (ID={app.selected_room_type_id}).",
                text_color="#16a34a"
            )
            # Başarılı işlem sonrası temizleme ve yenileme
            clear_room_type_form(app)
            build_room_type_list(app)
            if hasattr(app, 'build_room_cards'): app.build_room_cards()
        else:
            # DB'den False döndüğünde (örneğin, bu tipte aktif odalar varsa)
            app.label_rt_message.configure(
                text="❌ Oda tipi silinemedi. Bu tipe bağlı odalar bulunuyor olabilir.",
                text_color="#dc2626"
            )
            
    except Exception as e:
        app.label_rt_message.configure(
            text=f"❌ Silme işleminde beklenmedik hata: {e}",
            text_color="#dc2626"
        )


# --- UYGULAMA SINIFI VE ENTEGRASYON (Çalışması için gerekli olan yapı) ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- UI Yapılandırması ---
        self.title("Hotel Yönetim Paneli - Oda Tipleri")
        self.geometry("1000x800")
        ctk.set_appearance_mode("light") 

        # --- Ant Design Renk ve Font Tanımları ---
        self.color_card = "#ffffff" # Beyaz Kart
        self.color_panel = "#fafafa" # Çok Açık Gri Panel
        self.color_bg = "#f0f2f5" # Arka plan (Ana Ant Design arkaplan rengi)
        
        self.font_normal = ("Poppins", 12)
        self.font_title = ("Poppins", 18, "bold")
        self.font_subtitle = ("Poppins", 12)

        # --- Uygulama Durumu Değişkenleri ---
        self.selected_room_type_id = None
        self.entry_rt_name = None
        self.entry_rt_desc = None
        self.entry_rt_price = None
        self.entry_rt_capacity = None
        self.label_rt_message = None
        self.btn_rt_save = None
        self.btn_rt_delete = None
        self.room_types_scroll = None
        
        # Fonksiyonları App sınıfına bağla
        self.build_room_type_list = lambda: build_room_type_list(self)
        self.load_room_type_into_form = lambda *args: load_room_type_into_form(self, *args)
        self.save_room_type = lambda: save_room_type(self)
        self.delete_room_type = lambda: delete_room_type(self)
        
        # Harici Oda Kartları Fonksiyonu (Tanımlı olduğu varsayılır, yoksa boş geçer)
        self.build_room_cards = lambda: None 

        # Ana Ekranı oluştur
        self.configure(fg_color=self.color_bg)
        self.main_frame = ctk.CTkFrame(self, fg_color=self.color_bg)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Oda Tipleri Frame'ini yükle
        room_types_frame = create_room_types_frame(self, self.main_frame)
        room_types_frame.pack(fill="both", expand=True)

# --- Uygulamayı Çalıştır ---
if __name__ == "__main__":
    # Bu kısmı kendi projenizde test etmek için çalıştırmalısınız.
    # Önemli: Gerçek 'backend.services.hotel_service' modülünüzün erişilebilir olduğundan emin olun.
    # Eğer test amaçlı çalıştırmak isterseniz, bir önceki yanıttaki DummyHotelService'i kullanabilirsiniz.
    
    # app = App()
    # app.mainloop()
    pass # mainloop çağrısı bu ortamda hata vereceği için pas geçilmiştir.