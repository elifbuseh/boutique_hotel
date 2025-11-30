import customtkinter as ctk
import tkinter as tk
from datetime import date, datetime, timedelta 
from backend.services import hotel_service as db


def create_reservations_frame(app, parent):
    """
    Rezervasyon Yönetimi Ekranının ana çerçevesini ve yeni rezervasyon formunu oluşturur.
    """
    frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=app.color_card)
    frame.columnconfigure(0, weight=1)

    # --- Başlık Alanı ---
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=(15, 5))
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(1, weight=0)

    title = ctk.CTkLabel(header_frame, text="🗓️ Rezervasyon Yönetimi", font=app.font_title, text_color=app.color_text_main)
    title.grid(row=0, column=0, sticky="w")

    subtitle = ctk.CTkLabel(
        header_frame,
        text="Yeni rezervasyon oluşturun veya mevcut rezervasyonları yönetin.",
        font=app.font_subtitle,
        text_color="#6b7280"
    )
    subtitle.grid(row=1, column=0, sticky="w")

    btn_new_res = ctk.CTkButton(
        header_frame,
        text=" Yeni Rezervasyon",
        font=app.font_normal,
        fg_color=app.color_accent,
        hover_color=app.color_accent_alt,
        text_color="white", 
        command=lambda: app.show_reservations_view(),
    )
    btn_new_res.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="e")

    # --- Yeni Rezervasyon Formu ---
    form_card = ctk.CTkFrame(frame, corner_radius=12, fg_color=app.color_panel, border_color="#d1d5db", border_width=1)
    form_card.pack(fill="x", padx=20, pady=(5, 15))
    
    ctk.CTkLabel(form_card, text="Rezervasyon Detayları", font=("Poppins", 14, "bold"), text_color=app.color_text_main).grid(row=0, column=0, columnspan=6, padx=15, pady=(10, 5), sticky="w")

    form_card.columnconfigure((0, 2, 4), weight=0)
    form_card.columnconfigure((1, 3), weight=1)
    form_card.columnconfigure(5, weight=2)

    row_index = 1
    
    lbl_guest = ctk.CTkLabel(form_card, text="Misafir:", font=app.font_normal, text_color="#111827")
    lbl_guest.grid(row=row_index, column=0, padx=(15, 5), pady=8, sticky="w")
    app.combo_res_guest = ctk.CTkComboBox(form_card, width=220, font=app.font_normal, values=[], state="readonly")
    app.combo_res_guest.grid(row=row_index, column=1, padx=(0, 15), pady=8, sticky="ew")

    lbl_room = ctk.CTkLabel(form_card, text="Oda:", font=app.font_normal, text_color="#111827")
    lbl_room.grid(row=row_index, column=2, padx=(15, 5), pady=8, sticky="w")
    app.combo_res_room = ctk.CTkComboBox(
        form_card, width=220, font=app.font_normal, values=[], state="readonly", command=app.on_room_change
    )
    app.combo_res_room.grid(row=row_index, column=3, padx=(0, 15), pady=8, sticky="ew")
    row_index += 1

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year, current_year + 6)]
    months = [f"{m:02d}" for m in range(1, 13)]
    days = [f"{d:02d}" for d in range(1, 32)]
    
    lbl_ci_co = ctk.CTkLabel(form_card, text="Giriş / Çıkış:", font=app.font_normal, text_color="#111827")
    lbl_ci_co.grid(row=row_index, column=0, padx=(15, 5), pady=8, sticky="w")
    
    date_frame_combined = ctk.CTkFrame(form_card, fg_color="transparent")
    date_frame_combined.grid(row=row_index, column=1, columnspan=4, padx=(0, 15), pady=8, sticky="w")
    
    ctk.CTkLabel(date_frame_combined, text="Giriş:", font=app.font_normal).pack(side="left", padx=(0, 5))
    app.cb_ci_year = ctk.CTkComboBox(date_frame_combined, width=70, values=years, state="readonly", font=app.font_normal)
    app.cb_ci_year.pack(side="left", padx=2)
    app.cb_ci_month = ctk.CTkComboBox(date_frame_combined, width=55, values=months, state="readonly", font=app.font_normal)
    app.cb_ci_month.pack(side="left", padx=2)
    app.cb_ci_day = ctk.CTkComboBox(date_frame_combined, width=55, values=days, state="readonly", font=app.font_normal)
    app.cb_ci_day.pack(side="left", padx=(2, 20))
    app.cb_ci_year.set(str(datetime.now().year))
    app.cb_ci_month.set(f"{datetime.now().month:02d}")
    app.cb_ci_day.set(f"{datetime.now().day:02d}")

    tomorrow = datetime.now() + timedelta(days=1)
    ctk.CTkLabel(date_frame_combined, text="Çıkış:", font=app.font_normal).pack(side="left", padx=(20, 5))
    app.cb_co_year = ctk.CTkComboBox(date_frame_combined, width=70, values=years, state="readonly", font=app.font_normal)
    app.cb_co_year.pack(side="left", padx=2)
    app.cb_co_month = ctk.CTkComboBox(date_frame_combined, width=55, values=months, state="readonly", font=app.font_normal)
    app.cb_co_month.pack(side="left", padx=2)
    app.cb_co_day = ctk.CTkComboBox(date_frame_combined, width=55, values=days, state="readonly", font=app.font_normal)
    app.cb_co_day.pack(side="left", padx=2)

    app.cb_co_year.set(str(tomorrow.year))
    app.cb_co_month.set(f"{tomorrow.month:02d}")
    app.cb_co_day.set(f"{tomorrow.day:02d}")
    
    row_index += 1

    lbl_price = ctk.CTkLabel(form_card, text="Gecelik Ücret:", font=app.font_normal, text_color="#111827")
    lbl_price.grid(row=row_index, column=0, padx=(15, 5), pady=8, sticky="w")
    app.entry_res_price = ctk.CTkEntry(form_card, width=150, font=app.font_normal, placeholder_text="0.00", fg_color="#f5f5f5")
    app.entry_res_price.grid(row=row_index, column=1, padx=(0, 15), pady=8, sticky="w")

    app.label_res_message = ctk.CTkLabel(form_card, text="", font=("Poppins", 11), text_color="#dc2626")
    app.label_res_message.grid(row=row_index, column=2, columnspan=2, padx=15, pady=(4, 4), sticky="w")

    btn_save_res = ctk.CTkButton(
        form_card,
        text="Rezervasyonu Tamamla",
        font=app.font_normal,
        fg_color=app.color_accent,
        hover_color=app.color_accent_alt,
        text_color="white",
        command=app.save_reservation
    )
    btn_save_res.grid(row=row_index, column=5, columnspan=1, padx=(15, 15), pady=8, sticky="e")
    row_index += 1


    # --- Rezervasyon Listesi ---
    app.reservations_scroll = ctk.CTkScrollableFrame(
        frame,
        corner_radius=12,
        width=900,
        height=320,
        fg_color=app.color_panel,
        label_text="Mevcut Rezervasyonlar",
        label_font=("Poppins", 14, "bold"),
        label_text_color=app.color_text_main
    )
    app.reservations_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    app.label_total_revenue = ctk.CTkLabel(
        frame,
        text="Toplam Odeme: 0 ₺",
        font=("Poppins", 12, "bold"),
        text_color=app.color_text_main,
        fg_color="transparent"
    )
    app.label_total_revenue.pack(anchor="e", padx=30, pady=(0, 10))

    app.build_reservations_list()
    app.refresh_reservation_choices()
    return frame


def refresh_reservation_choices(app):
    """Misafir ve Oda ComboBox'larını günceller. Sadece 3 değer (id, ad, soyad) bekler."""
    app.guest_choice_map = {}
    
    guests = db.get_guests_without_reservation() 
    guest_display_list = []
    
    for gid, first_name, last_name in guests:
        label = f"{first_name} {last_name}"
        guest_display_list.append(label)
        app.guest_choice_map[label] = gid
    
    if guest_display_list:
        app.combo_res_guest.configure(values=guest_display_list)
        app.combo_res_guest.set(guest_display_list[0])
    else:
        app.combo_res_guest.configure(values=["Misafir yok"])
        app.combo_res_guest.set("Misafir yok")

    app.room_choice_map = {}
    rooms = db.get_free_rooms() 
    room_display_list = []
    for rid, room_no, room_type in rooms:
        label = f"#{room_no} ({room_type})"
        room_display_list.append(label)
        app.room_choice_map[label] = rid
        
    if room_display_list:
        app.combo_res_room.configure(values=room_display_list)
        app.combo_res_room.set(room_display_list[0])
        app.on_room_change(room_display_list[0])
    else:
        app.combo_res_room.configure(values=["Bos oda yok"])
        app.combo_res_room.set("Bos oda yok")
        app.entry_res_price.delete(0, "end")


def on_room_change(app, selected_label: str):
    """Oda seçimi değiştiğinde fiyatı günceller."""
    room_id = app.room_choice_map.get(selected_label)
    if not room_id:
        app.entry_res_price.delete(0, "end")
        return
    
    price = db.get_nightly_price_for_room(room_id)
    if price is not None:
        app.entry_res_price.delete(0, "end")
        app.entry_res_price.insert(0, str(price))


def get_status_tag_colors(status: str):
    """Duruma göre renk ve metin döndürür (Ant Design Tag benzetmesi)."""
    status_upper = status.upper()
    if status_upper == 'CANCELLED':
        return {"color": "#fecaca", "text_color": "#991b1b", "text": "İPTAL EDİLDİ"}
    elif status_upper == 'CONFIRMED':
        return {"color": "#bfdbfe", "text_color": "#1e40af", "text": "ONAYLANDI"}
    elif status_upper == 'CHECKED_IN':
        return {"color": "#fcd34d", "text_color": "#92400e", "text": "GİRİŞ YAPTI"}
    elif status_upper == 'CHECKED_OUT':
        return {"color": "#a7f3d0", "text_color": "#065f46", "text": "ÇIKIŞ YAPTI"}
    else:
        return {"color": "#e5e7eb", "text_color": "#374151", "text": status_upper}


def build_reservations_list(app):
    """
    Tüm rezervasyonları listeler ve her satır için CRUD butonlarını ekler.
    Tablo sütunları sabit genişlik ile düzenlendi ve hizalamalar iyileştirildi.
    """
    for child in app.reservations_scroll.winfo_children():
        child.destroy()

    reservations = db.get_all_reservations()
    if not reservations:
        lbl = ctk.CTkLabel(
            app.reservations_scroll,
            text="Henüz rezervasyon kaydi yok.",
            font=app.font_normal,
            text_color=app.color_text_main
        )
        lbl.pack(pady=40)
        app.label_total_revenue.configure(text="Toplam Ödeme: 0 ₺")
        return

    # --- BAŞLIK ÇUBUĞU (Hata Düzeltme) ---
    header = ctk.CTkFrame(app.reservations_scroll, fg_color=app.color_sidebar_light, corner_radius=8)
    header.pack(fill="x", padx=10, pady=(8, 4))

    # Genişlikler: Misafir hariç sabit, İşlemler 140
    cols = ["ID", "Misafir", "Oda", "Giriş", "Çıkış", "Tutar", "Durum", "İşlemler"]
    widths = [30, 180, 70, 90, 90, 80, 100, 140] 
    PADDING = 5 # Tek bir genel padding değeri

    for i, (col, w) in enumerate(zip(cols, widths)):
        lbl = ctk.CTkLabel(
            header,
            text=col,
            font=("Poppins", 11, "bold"),
            text_color="#111827",
            width=w,
            anchor="w"
        )
        
        # Başlık Hizalama: Misafir hariç sağa hizalanan sütunları kontrol et.
        if col in ["Tutar", "Durum", "İşlemler"]:
             lbl.grid(row=0, column=i, padx=PADDING, pady=6, sticky="e")
        else:
             lbl.grid(row=0, column=i, padx=PADDING, pady=6, sticky="w")

    # Misafir sütununa (index 1) esneklik verilir.
    for i in range(len(cols)):
        header.grid_columnconfigure(i, weight=1 if i == 1 else 0)


    total_sum = 0.0
    for r in reservations:
        res_id, guest_name, room_number, ci, co, status, total_amount = r
        
        # --- SATIR ÇERÇEVESİ ---
        # Tek tek satırların arka plan rengini ayarlayarak daha belirgin yapabiliriz.
        row_frame = ctk.CTkFrame(
            app.reservations_scroll, 
            fg_color=app.color_card, 
            corner_radius=8, 
            border_color="#e5e7eb", 
            border_width=1
        )
        row_frame.pack(fill="x", padx=10, pady=3)
        for i in range(len(cols)):
            row_frame.grid_columnconfigure(i, weight=1 if i == 1 else 0)

        if total_amount is not None:
            total_sum += float(total_amount)

        status_info = get_status_tag_colors(status)

        data_values = [
            str(res_id),
            guest_name,
            f"#{room_number}",
            ci.strftime("%Y-%m-%d"),
            co.strftime("%Y-%m-%d"),
            f"{float(total_amount):.2f} ₺" if total_amount is not None else "0.00 ₺"
        ]

        for i, val in enumerate(data_values):
            col_name = cols[i]
            
            if i == 1:
                # Misafir Adı (Tıklanabilir)
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=f"👤 {val}",
                    font=("Poppins", 11, "bold"),
                    text_color="#1890ff",
                    width=widths[i],
                    anchor="w",
                    cursor="hand2"
                )
                lbl.bind("<Button-1>", lambda event, rid=res_id: app.toggle_expenses_popup(rid, force_show=True))
                sticky_val = "w"
            else:
                # Diğer sabit veri sütunları
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=val,
                    font=app.font_normal,
                    text_color=app.color_text_main if col_name != "Tutar" else "#16a34a",
                    width=widths[i],
                    anchor="w"
                )
                # Tutar sütununu sağa hizala
                sticky_val = "e" if col_name == "Tutar" else "w"
            
            lbl.grid(row=0, column=i, padx=PADDING, pady=6, sticky=sticky_val)
        
        # Durum Sütunu (Tag Benzeri)
        status_lbl = ctk.CTkLabel(
            row_frame,
            text=status_info["text"],
            font=("Poppins", 10, "bold"),
            fg_color=status_info["color"],
            text_color=status_info["text_color"],
            corner_radius=6,
            width=widths[6]
        )
        status_lbl.grid(row=0, column=6, padx=PADDING, pady=6, sticky="e") 

        # İşlemler Sütunu (Butonlar)
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=7, padx=PADDING, pady=6, sticky="e") 
        
        BUTTON_WIDTH = 70 
        
        if status.upper() == "CONFIRMED":
            # Giriş Yap butonu (İşlevi bağlandı)
            btn_ci = ctk.CTkButton(
                action_frame,
                text="Giriş Yap",
                width=BUTTON_WIDTH, 
                font=("Poppins", 10, "bold"),
                fg_color="#27ae60",
                hover_color="#2ecc71",
                text_color="white",
                # Çalışması için handleCheckIn metodu app.py'de tanımlı olmalı
                command=lambda rid=res_id: app.handleCheckIn(rid) 
            )
            btn_ci.pack(side="left", padx=2, pady=2)
        elif status.upper() == "CHECKED_IN":
            # Çıkış Yap butonu (İşlevi bağlandı)
            btn_co = ctk.CTkButton(
                action_frame,
                text="Çıkış Yap",
                width=BUTTON_WIDTH, 
                font=("Poppins", 10, "bold"),
                fg_color="#e67e22",
                hover_color="#f39c12",
                text_color="white",
                # Çalışması için handleCheckOut metodu app.py'de tanımlı olmalı
                command=lambda rid=res_id: app.handleCheckOut(rid) 
            )
            btn_co.pack(side="left", padx=2, pady=2)
        
        if status.upper() in ["CONFIRMED", "CHECKED_IN"]:
             btn_cancel = ctk.CTkButton(
                action_frame,
                text="İptal",
                width=60,
                font=("Poppins", 10, "bold"),
                fg_color="#c0392b",
                hover_color="#e74c3c",
                text_color="white",
                command=lambda rid=res_id: app.cancel_reservation(rid)
            )
             btn_cancel.pack(side="left", padx=2, pady=2)


    app.label_total_revenue.configure(text=f"Toplam Odeme: {total_sum:.2f} ₺")


# --- Diğer Fonksiyonlar (Aynı Kaldı) ---

def save_reservation(app):
    """Yeni rezervasyon kaydeder."""
    guest_label = app.combo_res_guest.get()
    room_label = app.combo_res_room.get()

    if guest_label == "Misafir yok" or not guest_label:
        app.label_res_message.configure(text="Önce misafir eklemelisiniz.", text_color="#dc2626")
        return
    if room_label == "Bos oda yok" or not room_label:
        app.label_res_message.configure(text="Müsait oda bulunamadı.", text_color="#dc2626")
        return

    guest_id = app.guest_choice_map.get(guest_label)
    room_id = app.room_choice_map.get(room_label)

    try:
        ci_year = int(app.cb_ci_year.get())
        ci_month = int(app.cb_ci_month.get())
        ci_day = int(app.cb_ci_day.get())
        co_year = int(app.cb_co_year.get())
        co_month = int(app.cb_co_month.get())
        co_day = int(app.cb_co_day.get())
        check_in_date = date(ci_year, ci_month, ci_day)
        check_out_date = date(co_year, co_month, co_day)
    except Exception:
        app.label_res_message.configure(text="Tarih formatı hatalı.", text_color="#dc2626")
        return

    if check_out_date <= check_in_date:
        app.label_res_message.configure(text="Çıkış tarihi, giriş tarihinden sonra olmalı.", text_color="#dc2626")
        return
    
    if check_in_date < date.today():
        app.label_res_message.configure(text="Giriş tarihi geçmiş bir gün olamaz.", text_color="#dc2626")
        return

    price_str = app.entry_res_price.get().strip()
    try:
        nightly_price = float(price_str)
    except ValueError:
        app.label_res_message.configure(text="Gecelik ücret geçerli bir sayı olmalı.", text_color="#dc2626")
        return
    
    if db.room_has_conflict(room_id, check_in_date, check_out_date):
        app.label_res_message.configure(text="Seçilen tarihlerde bu oda zaten dolu.", text_color="#dc2626")
        return
    
    num_nights = (check_out_date - check_in_date).days
    total_price = nightly_price * num_nights

    new_id = db.insert_reservation(guest_id, room_id, check_in_date, check_out_date, nightly_price, total_price)
    if new_id is None:
        app.label_res_message.configure(text="Rezervasyon eklenirken hata oluştu.", text_color="#dc2626")
        return

    app.label_res_message.configure(text=f"Rezervasyon oluşturuldu (ID: {new_id}) 🎉", text_color="#16a34a")
    app.build_reservations_list()
    app.refresh_reservation_choices()
    app.build_room_cards() 
    app.refresh_dashboard()


def cancel_reservation(app, reservation_id: int):
    """Rezervasyonu iptal eder."""
    ok = db.update_reservation_status(reservation_id, "CANCELLED")
    if ok:
        app.label_res_message.configure(
            text=f"Rezervasyon iptal edildi (ID: {reservation_id}).",
            text_color="#16a34a"
        )
        app.build_reservations_list()
        app.refresh_reservation_choices()
        app.build_room_cards()
        app.refresh_dashboard()
    else:
        app.label_res_message.configure(
            text="Rezervasyon iptal edilirken hata oluştu.",
            text_color="#dc2626"
        )