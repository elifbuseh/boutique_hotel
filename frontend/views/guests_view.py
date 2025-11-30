import customtkinter as ctk
import tkinter.messagebox as mb
from backend.services import hotel_service as db


def create_guests_frame(app, parent):
    # Ana Misafir Yönetimi Çerçevesi
    frame = ctk.CTkFrame(parent, corner_radius=24, fg_color=app.color_card)

    title = ctk.CTkLabel(frame, text="Misafir Kayıtları Yönetimi", font=app.font_title, text_color="#111827")
    title.pack(pady=(15, 4), anchor="w", padx=25)

    subtitle = ctk.CTkLabel(
        frame,
        text="Yeni misafir ekleyebilir, duzenleyebilir veya silebilirsiniz.",
        font=app.font_subtitle,
        text_color="#6b7280"
    )
    subtitle.pack(pady=(0, 12), anchor="w", padx=25)
    
    # Yeni Misafir Ekle Butonu Kontrol Alanı
    top_controls_frame = ctk.CTkFrame(frame, fg_color="transparent")
    top_controls_frame.pack(fill="x", padx=20, pady=(5, 10))

    # Misafir Ekle Butonu (Modal'ı açar)
    app.btn_new_guest = ctk.CTkButton(
        top_controls_frame,
        text="➕ Yeni Misafir Ekle",
        font=("Poppins", 13, "bold"),
        fg_color=app.color_accent, 
        hover_color=app.color_accent,
        text_color="#f8fafc",
        corner_radius=12,
        height=38,
        command=lambda: app.toggle_guest_form(force_show=True)
    )
    app.btn_new_guest.pack(side="right", padx=0)
    
    # Misafir Listesi Alanı
    app.guests_scroll = ctk.CTkScrollableFrame(
        frame,
        corner_radius=16,
        width=900,
        height=350,
        fg_color=app.color_panel
    )
    app.guests_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    app.build_guest_list()
    return frame


def create_guest_form_content(app, parent):
    """
    Bu fonksiyon, Pop-up penceresi (CTkToplevel) içine form içeriğini yerleştirir.
    Parent, Toplevel penceresinin kendisidir.
    """
    
    # Formun ana içeriği
    form_frame = ctk.CTkFrame(parent, corner_radius=16, fg_color=app.color_panel)
    form_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Form başlığı
    app.form_guest_title = ctk.CTkLabel(
        form_frame,
        text="Yeni Misafir Ekle",
        font=("Poppins", 16, "bold"),
        text_color="#2c3e50" 
    )
    app.form_guest_title.grid(row=0, column=0, columnspan=5, padx=15, pady=(15, 10), sticky="w")
    
    # Form Alanları (Grid Yöneticisi)
    
    # 1. Row: Ad & Soyad
    label_first = ctk.CTkLabel(form_frame, text="Ad:", font=app.font_normal, text_color="#111827")
    label_first.grid(row=1, column=0, padx=(15, 5), pady=8, sticky="e")
    app.entry_guest_first_name = ctk.CTkEntry(form_frame, width=180, font=app.font_normal, placeholder_text="Ad", corner_radius=8)
    app.entry_guest_first_name.grid(row=1, column=1, padx=(5, 15), pady=8, sticky="w")

    label_last = ctk.CTkLabel(form_frame, text="Soyad:", font=app.font_normal, text_color="#111827")
    label_last.grid(row=1, column=2, padx=(15, 5), pady=8, sticky="e")
    app.entry_guest_last_name = ctk.CTkEntry(form_frame, width=180, font=app.font_normal, placeholder_text="Soyad", corner_radius=8)
    app.entry_guest_last_name.grid(row=1, column=3, padx=(5, 15), pady=8, sticky="w")

    # 2. Row: E-posta & Telefon
    label_email = ctk.CTkLabel(form_frame, text="E-posta:", font=app.font_normal, text_color="#111827")
    label_email.grid(row=2, column=0, padx=(15, 5), pady=8, sticky="e")
    app.entry_guest_email = ctk.CTkEntry(form_frame, width=180, font=app.font_normal, placeholder_text="ornek@mail.com", corner_radius=8)
    app.entry_guest_email.grid(row=2, column=1, padx=(5, 15), pady=8, sticky="w")

    label_phone = ctk.CTkLabel(form_frame, text="Telefon:", font=app.font_normal, text_color="#111827")
    label_phone.grid(row=2, column=2, padx=(15, 5), pady=8, sticky="e")
    app.entry_guest_phone = ctk.CTkEntry(form_frame, width=180, font=app.font_normal, placeholder_text="+90...", corner_radius=8)
    app.entry_guest_phone.grid(row=2, column=3, padx=(5, 15), pady=8, sticky="w")

    # 3. Row: T.C. No
    label_tc = ctk.CTkLabel(form_frame, text="T.C. Kimlik No:", font=app.font_normal, text_color="#111827")
    label_tc.grid(row=3, column=0, padx=(15, 5), pady=8, sticky="e")
    app.entry_guest_tc = ctk.CTkEntry(form_frame, width=180, font=app.font_normal, placeholder_text="11 haneli", corner_radius=8)
    app.entry_guest_tc.grid(row=3, column=1, padx=(5, 15), pady=8, sticky="w")
    
    # Boşluk bırakmak için ağırlık verilir
    form_frame.grid_columnconfigure(4, weight=1)
    
    # 4. Row: Mesaj Alanı
    app.label_guest_message = ctk.CTkLabel(form_frame, text="", font=("Poppins", 11), text_color="#dc2626")
    app.label_guest_message.grid(row=4, column=0, columnspan=4, padx=15, pady=(4, 15), sticky="w")
    
    # 5. Row: Kontrol Butonları (Sağa hizalı)
    button_controls = ctk.CTkFrame(form_frame, fg_color="transparent")
    # Butonları en sağa hizalamak için tüm sütunları kapsa ve sticky="e" kullan
    button_controls.grid(row=5, column=0, columnspan=4, padx=15, pady=8, sticky="e") 
    
    # İptal Butonu
    btn_cancel_guest = ctk.CTkButton(
        button_controls,
        text="İptal",
        font=("Poppins", 13, "bold"),
        fg_color="#cbd5e1", 
        hover_color="#94a3b8",
        text_color="#1f2937",
        corner_radius=12,
        height=38,
        command=app.close_guest_form # Pop-up'ı kapatır
    )
    btn_cancel_guest.pack(side="left", padx=(0, 10))

    # Kaydet Butonu
    app.btn_save_guest = ctk.CTkButton(
        button_controls,
        text="Kaydet",
        font=("Poppins", 13, "bold"),
        fg_color=app.color_accent, 
        hover_color=app.color_accent, 
        text_color="#f8fafc",
        corner_radius=12,
        height=38,
        command=app.save_guest
    )
    app.btn_save_guest.pack(side="left")


def build_guest_list(app):
    # Eski listeyi temizle
    for child in app.guests_scroll.winfo_children():
        child.destroy()

    guests = db.get_all_guests()
    if not guests:
        empty_label = ctk.CTkLabel(
            app.guests_scroll,
            text="Henuz misafir kaydi yok. Yeni misafir ekleyin.",
            font=app.font_normal,
            text_color="#6b7280"
        )
        empty_label.pack(pady=30)
        return

    # Liste Başlığı (Ant Design Table Header)
    header_frame = ctk.CTkFrame(app.guests_scroll, fg_color="#f3f4f6", corner_radius=12)
    header_frame.pack(fill="x", padx=5, pady=(8, 4))

    # Kolon Tanımları
    cols = ["ID", "Ad Soyad", "T.C. No", "Telefon", "E-posta", "İşlemler"]
    widths = [40, 200, 120, 140, 220, 180] 

    for i, (col, w) in enumerate(zip(cols, widths)):
        lbl = ctk.CTkLabel(
            header_frame,
            text=col,
            font=("Poppins", 11, "bold"),
            text_color="#1f2937",
            width=w,
            anchor="w"
        )
        lbl.grid(row=0, column=i, padx=10, pady=8, sticky="w")
        
        if i == len(cols) - 1:
             lbl.configure(anchor="e")


    # Misafir Verileri
    for g in guests:
        guest_id, first_name, last_name, email, phone, tc_no, is_blacklisted = g
        
        row_frame = ctk.CTkFrame(app.guests_scroll, fg_color=app.color_card, corner_radius=12, border_width=1, border_color="#f3f4f6")
        row_frame.pack(fill="x", padx=5, pady=3)

        full_name = f"{first_name} {last_name}"
        values = [str(guest_id), full_name, tc_no or "-", phone or "-", email or "-"]

        # Renkli etiketler (Ant Design Tag taklidi)
        colors = {
            2: {"text": tc_no or "-", "bg": "#eff6ff", "fg": "#1e40af"},  # TC No (Mavi Ton)
            3: {"text": phone or "-", "bg": "#f0fdf4", "fg": "#15803d"},  # Telefon (Yeşil Ton)
            4: {"text": email or "-", "bg": "#fefce8", "fg": "#ca8a04"},  # E-posta (Sarı Ton)
        }


        for i, (val, w) in enumerate(zip(values, widths[:-1])):
            text_color = "#111827"
            bg_color = "transparent"
            
            if i in colors and val != "-":
                text_color = colors[i]["fg"]
                bg_color = colors[i]["bg"]
            
            if i == 1:
                font = ("Poppins", 12, "bold")
            else:
                font = app.font_normal

            current_padx = 10
            if i == 0:
                current_padx = (15, 5)
            elif i == 1:
                current_padx = 0
            
            lbl = ctk.CTkLabel(
                row_frame,
                text=val,
                font=font,
                text_color=text_color,
                fg_color=bg_color if i in colors and val != "-" else "transparent",
                corner_radius=8,
                width=w,
                anchor="w"
            )
            lbl.grid(row=0, column=i, padx=current_padx, pady=6, sticky="w")


        # Aksiyon Butonları
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=len(values), padx=10, pady=6, sticky="e")

        # Düzenle Butonu
        btn_edit = ctk.CTkButton(
            action_frame,
            text="Düzenle",
            width=80,
            font=("Poppins", 11, "bold"),
            fg_color="#bfdbfe",
            hover_color="#93c5fd",
            text_color="#1d4ed8",
            corner_radius=12,
            command=lambda gid=guest_id: app.populate_guest_form(gid)
        )
        btn_edit.pack(side="left", padx=5)

        # Sil Butonu
        btn_del = ctk.CTkButton(
            action_frame,
            text="Sil",
            width=60,
            font=("Poppins", 11, "bold"),
            fg_color="#fee2e2",
            hover_color="#fecaca",
            text_color="#b91c1c",
            corner_radius=12,
            command=lambda gid=guest_id, full_name=full_name: mb.askyesno("Misafir Kaydını Sil", f"'{full_name}' misafirini silmek istediğinizden emin misiniz?") and app.delete_guest(gid)
        )
        btn_del.pack(side="left", padx=5)


def populate_guest_form(app, guest_id):
    """Düzenleme modunda pop-up formu doldurur."""
    guest = db.get_guest_by_id(guest_id)
    if not guest:
        if app.guest_form_popup:
            app.label_guest_message.configure(text="❌ Misafir bulunamadi.", text_color="#dc2626")
        return

    guest_id, first_name, last_name, email, phone, tc_no, _ = guest

    app.selected_guest_id = guest_id
    
    # Form alanlarını doldur
    app.entry_guest_first_name.delete(0, "end")
    app.entry_guest_first_name.insert(0, first_name or "")
    
    app.entry_guest_last_name.delete(0, "end")
    app.entry_guest_last_name.insert(0, last_name or "")
    
    app.entry_guest_email.delete(0, "end")
    app.entry_guest_email.insert(0, email or "")
    
    app.entry_guest_phone.delete(0, "end")
    app.entry_guest_phone.insert(0, phone or "")
    
    app.entry_guest_tc.delete(0, "end")
    app.entry_guest_tc.insert(0, tc_no or "")
    
    # Pop-up açıkken mesaj ve buton güncellemesi yap
    if app.guest_form_popup:
        app.guest_form_popup.title(f"Misafiri Düzenle (ID: {guest_id})")
        app.form_guest_title.configure(text=f"Misafiri Düzenle (ID: {guest_id})")
        app.label_guest_message.configure(
            text="",
            text_color="#6b7280"
        )
        app.btn_save_guest.configure(text="Güncelle")


def save_guest(app):
        first_name = app.entry_guest_first_name.get().strip()
        last_name = app.entry_guest_last_name.get().strip()
        email = app.entry_guest_email.get().strip() or None
        phone = app.entry_guest_phone.get().strip() or None
        tc_no = app.entry_guest_tc.get().strip() or None

        if not first_name or not last_name:
            if app.guest_form_popup:
                app.label_guest_message.configure(text="Ad ve Soyad zorunludur.", text_color="#dc2626")
            else:
                mb.showerror("Hata", "Ad ve Soyad zorunludur.")
            return

        if app.selected_guest_id is not None:
            ok = db.update_guest(app.selected_guest_id, first_name, last_name, email, phone, tc_no)
            if ok:
                if app.guest_form_popup:
                    app.label_guest_message.configure(
                        text=f"✅ Misafir basariyla guncellendi (ID: {app.selected_guest_id})",
                        text_color="#16a34a"
                    )
                app.build_guest_list()
                app.close_guest_form() # Başarılıysa pop-up'ı kapat
            else:
                if app.guest_form_popup:
                    app.label_guest_message.configure(
                        text="❌ Misafir guncellenirken hata olustu.",
                        text_color="#dc2626"
                    )
                else:
                    mb.showerror("Hata", "Misafir güncellenirken hata oluştu.")
            return

        new_id = db.insert_guest(first_name, last_name, email, phone, tc_no)
        if new_id is not None:
            if app.guest_form_popup:
                app.label_guest_message.configure(
                    text=f"✅ Misafir basariyla eklendi (ID: {new_id})",
                    text_color="#16a34a"
                )
            app.build_guest_list()
            app.close_guest_form() # Başarılıysa pop-up'ı kapat
        else:
            if app.guest_form_popup:
                app.label_guest_message.configure(
                    text="❌ Misafir eklenirken bir hata olustu.",
                    text_color="#dc2626"
                )
            else:
                mb.showerror("Hata", "Misafir eklenirken bir hata oluştu.")


def delete_guest(app, guest_id: int):
        ok = db.delete_guest(guest_id)
        if ok:
            app.build_guest_list()
        else:
            mb.showerror("Hata", "Misafir silinemedi. (Aktif rezervasyonu olabilir.)")