import tkinter as tk
import customtkinter as ctk
from backend.services import hotel_service as db
# timedelta import'u app.py'de olduğu için buraya gerek yoktur, ancak genel kullanım için ekleyebiliriz.


# --- YARDIMCI FONKSİYONLAR (CustomTkinter'a Uyarlanmış Renkler) ---

def get_gradient_color(app, status: str) -> str:
    """Duruma göre CustomTkinter'a uygun renk (Degrade yerine düz renk/yakın ton) döndürür."""
    status_upper = status.upper()
    
    # Yeşil (AVAILABLE/CLEAN)
    if status_upper in ('AVAILABLE', 'CLEAN'):
        return "#2ecc71" # Kızağa çekilmiş yeşil ton
    # Kırmızı (OCCUPIED)
    elif status_upper == 'OCCUPIED':
        return "#e74c3c" # Kırmızı
    # Turuncu (DIRTY)
    elif status_upper == 'DIRTY':
        return "#f39c12" # Turuncu
    # Gri (MAINTENANCE)
    elif status_upper == 'MAINTENANCE':
        return "#7f8c8d" # Gri
    # Mavi (Default)
    else:
        return "#3498db"

def get_status_tag_colors_text(status: str) -> dict:
    """Duruma göre metin, arka plan ve ön plan rengini döndürür."""
    status_upper = status.upper()
    if status_upper in ('AVAILABLE', 'CLEAN'):
        return {"bg": "#e6f8ee", "text": "MÜSAİT", "fg": "#27ae60"}
    elif status_upper == 'OCCUPIED':
        return {"bg": "#fde8e7", "text": "DOLU", "fg": "#e74c3c"}
    elif status_upper == 'DIRTY':
        return {"bg": "#fff4e5", "text": "TEMİZLİK GEREKİYOR", "fg": "#f39c12"}
    elif status_upper == 'MAINTENANCE':
        return {"bg": "#e5e7eb", "text": "BAKIMDA", "fg": "#7f8c8d"}
    else:
        return {"bg": "#eee", "text": status_upper, "fg": "#555"}


# --- ANA FRAME OLUŞTURMA ---

def create_rooms_frame(app, parent):
    frame = ctk.CTkFrame(parent, corner_radius=24, fg_color=app.color_card)

    title = ctk.CTkLabel(
        frame,
        text="🏠 Oda Yönetimi",
        font=app.font_title,
        text_color="#111827"
    )
    title.pack(pady=(15, 4), anchor="w", padx=25)

    subtitle = ctk.CTkLabel(
        frame,
        text="Oda durumlarını buradan takip edebilir, hızlıca güncelleyebilirsiniz.",
        font=app.font_subtitle,
        text_color="#6b7280"
    )
    subtitle.pack(pady=(0, 12), anchor="w", padx=25)

    app.rooms_scroll = ctk.CTkScrollableFrame(
        frame,
        corner_radius=24,
        width=900,
        height=520,
        fg_color=app.color_panel
    )
    app.rooms_scroll.pack(fill="both", expand=True, padx=20, pady=10)

    app.build_room_cards()
    return frame

# --- ODA KARTLARINI OLUŞTURMA ---

def build_room_cards(app):
    for child in app.rooms_scroll.winfo_children():
        child.destroy()

    rooms = db.get_all_rooms()
    if not rooms:
        empty_label = ctk.CTkLabel(
            app.rooms_scroll,
            text="Hiç oda bulunamadı.",
            font=app.font_normal,
            text_color="#111827"
        )
        empty_label.pack(pady=20)
        return

    floors = {}
    for r in rooms:
        # room_id, room_no, room_type_name, floor_number, status
        room_id, room_no, room_type, floor, status = r
        floors.setdefault(floor, []).append(r)

    for floor in sorted(floors.keys()):
        # Kat Başlığı
        floor_label = ctk.CTkLabel(
            app.rooms_scroll,
            text=f"{floor}. KAT",
            font=("Poppins", 16, "bold"),
            text_color="#555555"
        )
        floor_label.pack(anchor="w", padx=18, pady=(18, 6))

        floor_frame = ctk.CTkFrame(app.rooms_scroll, fg_color="transparent")
        floor_frame.pack(fill="x", padx=10, pady=(0, 8))

        for i in range(len(floors[floor])):
            floor_frame.grid_columnconfigure(i, weight=1)

        for idx, r in enumerate(floors[floor]):
            room_id, room_no, room_type, f, status = r
            
            bg_color = get_gradient_color(app, status)
            status_info = get_status_tag_colors_text(status)

            def bind_card_click(widget, rid=room_id):
                widget.bind("<Button-1>", lambda e, rid=rid: app.open_status_menu(e, rid))

            # --- ODA KARTI ---
            card = ctk.CTkFrame(
                floor_frame,
                width=220,
                height=130,
                corner_radius=15, 
                fg_color=bg_color,
                cursor="hand2",
                border_width=0,
            )
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            bind_card_click(card)

            # Oda Tipi
            type_label = ctk.CTkLabel(
                card,
                text=room_type.upper(),
                font=("Poppins", 12),
                text_color="white", 
                fg_color="transparent"
            )
            type_label.pack(anchor="w", padx=15, pady=(10, 0))
            bind_card_click(type_label)

            # Oda Numarası (Büyük Font)
            number_label = ctk.CTkLabel(
                card,
                text=f"#{room_no}",
                font=("Poppins", 28, "bold"),
                text_color="white",
                fg_color="transparent"
            )
            number_label.pack(anchor="w", padx=15, pady=(2, 0))
            bind_card_click(number_label)

            # Durum Etiketi (Badge/Tag)
            status_badge = ctk.CTkLabel(
                card,
                text=status_info["text"],
                font=("Poppins", 12, "bold"),
                corner_radius=20,
                fg_color="#FFFFFF", # Düzeltildi: Opak Beyaz Hex kodu kullanıldı
                text_color="#111827", 
                padx=12,
                pady=4
            )
            status_badge.pack(anchor="w", padx=15, pady=(4, 0))
            bind_card_click(status_badge)
            
            # Rezervasyon butonu
            if status.upper() in ('AVAILABLE', 'CLEAN'):
                 btn_res = ctk.CTkButton(
                    card,
                    text="Rezervasyon Yap",
                    font=("Poppins", 10),
                    fg_color=app.color_accent, 
                    hover_color=app.color_accent_alt,
                    text_color="white",
                    height=20,
                    width=100,
                    command=lambda rid=room_id: app.open_reservation_for_room(rid)
                )
                 btn_res.pack(anchor="w", padx=15, pady=(6, 6))

# --- ODA DETAY POP-UP'I (MODAL) ---

def set_status(new_status, modal, app, rid):
    """Durumu günceller ve modalı kapatır."""
    ok = db.update_room_status(rid, new_status)
    if ok:
        app.build_room_cards()
        app.refresh_reservation_choices()
        modal.destroy()
    else:
        # Hata mesajı göster (mb.showerror veya benzeri)
        pass


def open_status_menu(app, event, room_id: int):
    """
    Oda kartına tıklanınca açılan modern oda detay pop-up'ı (CTkToplevel).
    """
    if app.status_popup is not None:
        try:
            app.status_popup.destroy()
        except Exception:
            pass
        app.status_popup = None

    try:
        room_data = db.get_room_details(room_id)
        if room_data and len(room_data) >= 4:
            _, room_no, room_type, status = room_data
        else:
            raise ValueError("Oda bilgisi eksik veya hatalı.")
    except Exception:
        room_no = "?"
        room_type = ""
        status = "UNKNOWN"

    modal = ctk.CTkToplevel(app)
    modal.grab_set()
    modal.title(f"Oda #{room_no} Detayları")
    
    # Pencere konumunu fare imlecinin yakınında ayarla
    modal.geometry(f"360x380+{event.x_root - 180}+{event.y_root - 100}")
    modal.resizable(False, False)
    
    card_container = ctk.CTkFrame(modal, fg_color=app.color_card, corner_radius=0)
    card_container.pack(fill="both", expand=True)

    status_info = get_status_tag_colors_text(status)
    header_color = get_gradient_color(app, status)
    
    # ---------------------------------------------
    # 1. MODAL BAŞLIĞI (Durum Rengine Göre)
    # ---------------------------------------------
    header = ctk.CTkFrame(card_container, fg_color=header_color, corner_radius=0)
    header.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(header, text=str(room_type).upper(), font=("Poppins", 14), text_color="white").pack(pady=(15, 0))
    ctk.CTkLabel(header, text=f"#{room_no}", font=("Poppins", 30, "bold"), text_color="white").pack(pady=(0, 5))
    
    # Durum Tag
    status_badge = ctk.CTkLabel(header, text=status_info["text"], font=("Poppins", 12, "bold"),
                                fg_color="#FFFFFF", text_color="#111827", corner_radius=20, padx=15, pady=4)
    status_badge.pack(pady=(0, 15))

    # ---------------------------------------------
    # 2. ANA İŞLEM BUTONU (Yeni Rezervasyon / Check-out)
    # ---------------------------------------------
    
    if status.upper() == 'OCCUPIED':
         btn_main_action = ctk.CTkButton(
            card_container,
            text="Check-Out Yap",
            font=("Poppins", 14, "bold"),
            fg_color="#c0392b", 
            hover_color="#e74c3c",
            text_color="white",
            height=40,
            command=lambda: set_status('DIRTY', modal, app, room_id)
        )
    else:
        btn_main_action = ctk.CTkButton(
            card_container,
            text="Yeni Rezervasyon Ekle",
            font=("Poppins", 14, "bold"),
            fg_color="#1890ff", 
            hover_color="#107ac9",
            text_color="white",
            height=40,
            state="disabled" if status.upper() in ('DIRTY', 'MAINTENANCE') else "normal", 
            command=lambda: app.open_reservation_for_room(room_id, modal)
        )
    btn_main_action.pack(pady=(5, 15), padx=20, fill="x")


    # ---------------------------------------------
    # 3. HIZLI DURUM DEĞİŞTİRME BUTONLARI
    # ---------------------------------------------
    
    ctk.CTkLabel(card_container, text="HIZLI DURUM DEGISTIR", font=("Poppins", 11, "bold"),
                 text_color="#6b7280").pack(pady=(0, 5))
    
    btn_container = ctk.CTkFrame(card_container, fg_color="transparent")
    btn_container.pack(pady=(0, 15), padx=15)

    # TEMİZ Butonu
    clean_info = get_status_tag_colors_text('CLEAN')
    btn_clean = ctk.CTkButton(btn_container, text=clean_info["text"], width=80, 
                              fg_color="transparent", border_width=2, 
                              border_color=clean_info["fg"], text_color=clean_info["fg"],
                              hover_color=clean_info["bg"], 
                              command=lambda: set_status("CLEAN", modal, app, room_id))
    btn_clean.grid(row=0, column=0, padx=5, pady=5)
    
    # KİRLİ Butonu
    dirty_info = get_status_tag_colors_text('DIRTY')
    btn_dirty = ctk.CTkButton(btn_container, text=dirty_info["text"], width=80, 
                              fg_color="transparent", border_width=2, 
                              border_color=dirty_info["fg"], text_color=dirty_info["fg"],
                              hover_color=dirty_info["bg"], 
                              command=lambda: set_status("DIRTY", modal, app, room_id))
    btn_dirty.grid(row=0, column=1, padx=5, pady=5)
    
    # BAKIM Butonu
    maint_info = get_status_tag_colors_text('MAINTENANCE')
    btn_maint = ctk.CTkButton(btn_container, text=maint_info["text"], width=80, 
                              fg_color="transparent", border_width=2, 
                              border_color=maint_info["fg"], text_color=maint_info["fg"],
                              hover_color=maint_info["bg"], 
                              command=lambda: set_status("MAINTENANCE", modal, app, room_id))
    btn_maint.grid(row=0, column=2, padx=5, pady=5)

    app.status_popup = modal


# --- REZERVASYON AÇMA ---

def open_reservation_for_room(app, room_id: int, modal_to_close=None):
    """Rezervasyon ekranını açar ve odayı seçili hale getirir."""
    app.show_reservations_view()
    app.refresh_reservation_choices()
    for label, rid in app.room_choice_map.items():
        if rid == room_id:
            app.combo_res_room.set(label)
            break
            
    room_label = app.combo_res_room.get()
    app.label_res_message.configure(
        text=f"Oda '{room_label}' için rezervasyon oluşturuyorsunuz.",
        text_color="#6b7280"
    )
    
    if modal_to_close:
        try:
            modal_to_close.destroy()
        except Exception:
            pass