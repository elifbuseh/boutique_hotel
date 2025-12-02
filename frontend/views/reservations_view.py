import customtkinter as ctk
from datetime import date, datetime, timedelta
from backend.services import hotel_service as db


def rebuild_guest_selectors(app, count: int, preset_labels=None):
    """Rebuild guest selection boxes based on desired count."""
    if not hasattr(app, "guest_selectors_frame"):
        return
    for child in app.guest_selectors_frame.winfo_children():
        child.destroy()
    app.guest_selectors = []
    values = getattr(app, "guest_selector_values", ["Misafir yok"])
    preset_labels = preset_labels or []
    for idx in range(max(1, count)):
        cb = ctk.CTkComboBox(
            app.guest_selectors_frame,
            width=220,
            font=app.font_normal,
            values=values,
            state="readonly",
        )
        cb.pack(fill="x", pady=2, padx=0)
        if idx < len(preset_labels):
            cb.set(preset_labels[idx])
        elif values:
            cb.set(values[0])
        app.guest_selectors.append(cb)
    if app.guest_selectors:
        app.combo_res_guest = app.guest_selectors[0]  # primary reference


def on_guest_count_change(app, value: str):
    """Triggered when guest count combobox changes."""
    try:
        desired = int(value)
    except Exception:
        desired = 1
    rebuild_guest_selectors(app, desired)


def create_reservations_frame(app, parent):
    """Rezervasyon Yönetimi ekranını oluşturur."""
    frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=app.color_card)
    frame.columnconfigure(0, weight=1)

    # Header
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=(15, 5))
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(1, weight=0)

    title = ctk.CTkLabel(header_frame, text="Rezervasyon Yönetimi", font=app.font_title, text_color=app.color_text_main)
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

    # Form
    form_card = ctk.CTkFrame(frame, corner_radius=12, fg_color=app.color_panel, border_color="#d1d5db", border_width=1)
    form_card.pack(fill="x", padx=20, pady=(5, 15))

    ctk.CTkLabel(form_card, text="Rezervasyon Detayları", font=("Poppins", 14, "bold"), text_color=app.color_text_main).grid(row=0, column=0, columnspan=6, padx=15, pady=(10, 5), sticky="w")

    form_card.columnconfigure(0, weight=0)  # misafir label
    form_card.columnconfigure(1, weight=2)  # misafir selector
    form_card.columnconfigure(2, weight=0)  # oda label
    form_card.columnconfigure(3, weight=2)  # oda combobox
    form_card.columnconfigure(4, weight=0)
    form_card.columnconfigure(5, weight=1)

    row_index = 1

    lbl_guest = ctk.CTkLabel(form_card, text="Misafir(ler):", font=app.font_normal, text_color="#111827")
    lbl_guest.grid(row=row_index, column=0, padx=(15, 5), pady=8, sticky="w")
    app.guest_selectors_frame = ctk.CTkFrame(form_card, fg_color="transparent")
    app.guest_selectors_frame.grid(row=row_index, column=1, padx=(0, 15), pady=8, sticky="ew")
    app.guest_selector_values = []
    app.guest_selectors = []
    rebuild_guest_selectors(app, 1)

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
    now = datetime.now()
    app.cb_ci_year.set(str(now.year))
    app.cb_ci_month.set(f"{now.month:02d}")
    app.cb_ci_day.set(f"{now.day:02d}")

    tomorrow = now + timedelta(days=1)
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

    lbl_guest_count = ctk.CTkLabel(form_card, text="Kişi Sayısı:", font=app.font_normal, text_color="#111827")
    lbl_guest_count.grid(row=row_index, column=2, padx=(15, 5), pady=8, sticky="w")
    app.combo_guest_count = ctk.CTkComboBox(
        form_card,
        width=120,
        font=app.font_normal,
        values=["1"],
        state="readonly",
        command=lambda val: on_guest_count_change(app, val),
    )
    app.combo_guest_count.grid(row=row_index, column=3, padx=(0, 15), pady=8, sticky="w")
    app.combo_guest_count.set("1")

    # Message row
    row_index += 1
    app.label_res_message = ctk.CTkLabel(form_card, text="", font=("Poppins", 11), text_color="#dc2626")
    app.label_res_message.grid(row=row_index, column=0, columnspan=4, padx=15, pady=(4, 4), sticky="w")

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
    app.btn_save_res = btn_save_res
    row_index += 1

    # Filters and list
    app.res_filter_state = "active"
    filter_frame = ctk.CTkFrame(frame, fg_color="transparent")
    filter_frame.pack(fill="x", padx=20, pady=(0, 6))

    def update_filter_styles(selected):
        buttons = {
            "active": app.btn_filter_active,
            "checked_out": app.btn_filter_checked_out,
            "cancelled": app.btn_filter_cancelled,
        }
        for key, btn in buttons.items():
            if not btn:
                continue
            if key == selected:
                btn.configure(fg_color=app.color_accent, text_color="white", hover_color=app.color_accent_alt)
            else:
                btn.configure(fg_color="#e5e7eb", text_color="#111827", hover_color="#d1d5db")

    def set_filter(filter_key: str):
        app.res_filter_state = filter_key
        update_filter_styles(filter_key)
        app.build_reservations_list()

    app.btn_filter_active = ctk.CTkButton(
        filter_frame,
        text="Mevcut",
        width=120,
        font=("Poppins", 11, "bold"),
        corner_radius=10,
        fg_color=app.color_accent,
        hover_color=app.color_accent_alt,
        text_color="white",
        command=lambda: set_filter("active")
    )
    app.btn_filter_active.pack(side="left", padx=(0, 6), pady=4)

    app.btn_filter_checked_out = ctk.CTkButton(
        filter_frame,
        text="Cikis Yapanlar",
        width=140,
        font=("Poppins", 11, "bold"),
        corner_radius=10,
        fg_color="#e5e7eb",
        hover_color="#d1d5db",
        text_color="#111827",
        command=lambda: set_filter("checked_out")
    )
    app.btn_filter_checked_out.pack(side="left", padx=6, pady=4)

    app.btn_filter_cancelled = ctk.CTkButton(
        filter_frame,
        text="Iptal Edilenler",
        width=140,
        font=("Poppins", 11, "bold"),
        corner_radius=10,
        fg_color="#e5e7eb",
        hover_color="#d1d5db",
        text_color="#111827",
        command=lambda: set_filter("cancelled")
    )
    app.btn_filter_cancelled.pack(side="left", padx=6, pady=4)

    update_filter_styles(app.res_filter_state)

    app.reservations_scroll = ctk.CTkScrollableFrame(
        frame,
        corner_radius=12,
        width=900,
        height=320,
        fg_color=app.color_panel
    )
    app.reservations_scroll.pack(fill="both", expand=True, padx=20, pady=(2, 12))

    app.label_total_revenue = ctk.CTkLabel(
        frame,
        text="Toplam Odeme: 0 TL",
        font=("Poppins", 12, "bold"),
        text_color=app.color_text_main,
        fg_color="transparent"
    )
    app.label_total_revenue.pack(anchor="e", padx=30, pady=(0, 10))

    app.build_reservations_list()
    app.refresh_reservation_choices()
    return frame


def refresh_reservation_choices(app):
    """Misafir ve Oda ComboBox'larını günceller."""
    app.guest_choice_map = getattr(app, "guest_choice_map", {})
    app.guest_id_to_label = getattr(app, "guest_id_to_label", {})

    # Mevcut seçimleri koru ki dolu misafirler de listede kalsın (düzenleme modu)
    existing_labels = [cb.get() for cb in getattr(app, "guest_selectors", [])] if hasattr(app, "guest_selectors") else []

    guests = db.get_guests_without_reservation()
    guest_display_list = []

    for gid, first_name, last_name in guests:
        label = f"{first_name} {last_name}"
        guest_display_list.append(label)
        app.guest_choice_map[label] = gid
        app.guest_id_to_label[gid] = label

    # Düzenlenen rezervasyondaki misafirleri de seçeneklere ekle
    for lbl in existing_labels:
        if lbl not in guest_display_list:
            guest_display_list.append(lbl)
        # label -> id eşleşmesi yoksa oluşturmaya çalış
        if lbl not in app.guest_choice_map:
            for gid, name in app.guest_id_to_label.items():
                if name == lbl:
                    app.guest_choice_map[lbl] = gid
                    break

    if guest_display_list:
        app.guest_selector_values = guest_display_list
    else:
        app.guest_selector_values = ["Misafir yok"]

    rebuild_guest_selectors(app, max(1, len(existing_labels)), preset_labels=existing_labels)

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
        if hasattr(app, "combo_guest_count"):
            app.combo_guest_count.configure(values=["1"])
            app.combo_guest_count.set("1")


def on_room_change(app, selected_label: str):
    """Oda seçimi değiştiğinde fiyatı ve kapasiteyi günceller."""
    room_id = app.room_choice_map.get(selected_label)
    if not room_id:
        app.entry_res_price.delete(0, "end")
        return

    price = db.get_nightly_price_for_room(room_id)
    if price is not None:
        app.entry_res_price.delete(0, "end")
        app.entry_res_price.insert(0, str(price))

    capacity = db.get_room_capacity(room_id)
    cap_val = capacity if capacity and capacity > 0 else 1
    options = [str(i) for i in range(1, cap_val + 1)]
    if hasattr(app, "combo_guest_count"):
        current_val = app.combo_guest_count.get()
        app.combo_guest_count.configure(values=options)
        if current_val not in options:
            app.combo_guest_count.set(options[-1])
        on_guest_count_change(app, app.combo_guest_count.get())


def get_status_tag_colors(status: str):
    status_upper = status.upper()
    if status_upper == 'CANCELLED':
        return {"color": "#fecaca", "text_color": "#991b1b", "text": "IPTAL EDILDI"}
    elif status_upper == 'CONFIRMED':
        return {"color": "#bfdbfe", "text_color": "#1e40af", "text": "ONAYLANDI"}
    elif status_upper == 'CHECKED_IN':
        return {"color": "#fcd34d", "text_color": "#92400e", "text": "GIRIS YAPTI"}
    elif status_upper == 'CHECKED_OUT':
        return {"color": "#a7f3d0", "text_color": "#065f46", "text": "CIKIS YAPTI"}
    else:
        return {"color": "#e5e7eb", "text_color": "#374151", "text": status_upper}


def build_reservations_list(app):
    for child in app.reservations_scroll.winfo_children():
        child.destroy()

    reservations = db.get_all_reservations()
    if not reservations:
        lbl = ctk.CTkLabel(
            app.reservations_scroll,
            text="Henuz rezervasyon kaydi yok.",
            font=app.font_normal,
            text_color=app.color_text_main
        )
        lbl.pack(pady=40)
        app.label_total_revenue.configure(text="Toplam Odeme: 0 TL")
        return

    # ID sütununu kaldırdık: sıra no + Misafir + Oda + tarih vs.
    cols = ["#", "Misafir", "Oda", "Giris", "Cikis", "Tutar", "Durum", "Islemler"]
    # Genişlikleri düzenledik: daha dar durum, daha geniş işlemler
    widths = [40, 230, 80, 105, 105, 110, 90, 250]
    padding = 8

    active = [r for r in reservations if (r[7] or "").upper() not in ("CANCELLED", "CHECKED_OUT")]
    checked_out = [r for r in reservations if (r[7] or "").upper() == "CHECKED_OUT"]
    cancelled = [r for r in reservations if (r[7] or "").upper() == "CANCELLED"]

    selected = getattr(app, "res_filter_state", "active")
    if selected == "checked_out":
        dataset = checked_out
        header_title = "Cikis Yapanlar"
    elif selected == "cancelled":
        dataset = cancelled
        header_title = "Iptal Edilenler"
    else:
        dataset = active
        header_title = "Mevcut Rezervasyonlar"
        selected = "active"

    # Tarihe (check-in) göre, sonra ID'ye göre sırala
    dataset = sorted(dataset, key=lambda r: (r[5], r[0]))

    def add_header(container, title):
        title_lbl = ctk.CTkLabel(
            container,
            text=title,
            font=("Poppins", 13, "bold"),
            text_color=app.color_text_main
        )
        title_lbl.pack(fill="x", padx=12, pady=(8, 2))

        header = ctk.CTkFrame(container, fg_color=app.color_sidebar_light, corner_radius=8)
        header.pack(fill="x", padx=12, pady=(2, 8))

        for i, (col, w) in enumerate(zip(cols, widths)):
            lbl = ctk.CTkLabel(
                header,
                text=col,
                font=("Poppins", 11, "bold"),
                text_color="#111827",
                width=w,
                anchor="w"
            )
            sticky_val = "e" if col in ["Tutar", "Durum", "Islemler"] else "w"
            lbl.grid(row=0, column=i, padx=padding, pady=4, sticky=sticky_val)
            header.grid_columnconfigure(i, weight=1 if i == 1 else 0)

    def add_row(container, res_index, res, row_state="active"):
        (
            res_id,
            primary_guest_id,
            room_id,
            guest_names_str,
            room_number,
            ci,
            co,
            status,
            total_amount,
            nightly_price,
            guest_count,
            guest_ids,
            guest_name_list,
        ) = res
        # Misafirleri ID'leriyle birlikte göster
        guest_display = "-"
        if guest_name_list and guest_ids and len(guest_name_list) == len(guest_ids):
            pairs = []
            for name, gid in zip(guest_name_list, guest_ids):
                pairs.append(f"{name} (ID:{gid})")
            guest_display = ", ".join(pairs)
        else:
            guest_display = guest_names_str or ", ".join(guest_name_list or []) or "-"
        is_cancelled = row_state == "cancelled"
        is_checked_out = row_state == "checked_out"
        status_to_show = "CANCELLED" if is_cancelled else status

        row_frame = ctk.CTkFrame(
            container,
            fg_color="#f3f4f6" if is_cancelled else app.color_card,
            corner_radius=8,
            border_color="#e5e7eb",
            border_width=1,
            height=48
        )
        row_frame.pack(fill="x", padx=12, pady=6)
        row_frame.pack_propagate(False)
        for i in range(len(cols)):
            row_frame.grid_columnconfigure(i, weight=0)

        # Misafirleri alt alta göstermek için \n ile ayrıştır
        guest_multiline = "\n".join(guest_display.split(", "))
        data_values = [
            str(res_index),
            guest_multiline,
            f"#{room_number}",
            ci.strftime("%Y-%m-%d"),
            co.strftime("%Y-%m-%d"),
            f"{float(total_amount):.2f} TL" if total_amount is not None else "0.00 TL",
            "",
            ""
        ]

        for i, val in enumerate(data_values):
            col_name = cols[i]
            if col_name in ["Durum", "Islemler"]:
                continue
            if col_name == "Misafir":
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=val,
                    font=("Poppins", 11, "bold"),
                    text_color="#1890ff" if not is_cancelled else "#9ca3af",
                    width=widths[i],
                    anchor="w",
                    cursor="hand2",
                    justify="left",
                )
                lbl.bind("<Button-1>", lambda event, rid=res_id: app.toggle_expenses_popup(rid, force_show=True))
                sticky_val = "w"
            else:
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=val,
                    font=app.font_normal,
                    text_color=app.color_text_main if not is_cancelled else "#9ca3af",
                    width=widths[i],
                    anchor="w"
                )
                sticky_val = "e" if col_name == "Tutar" else "w"
            lbl.grid(row=0, column=i, padx=padding, pady=4, sticky=sticky_val)

        status_info = get_status_tag_colors(status_to_show or "")
        status_lbl = ctk.CTkLabel(
            row_frame,
            text=status_info["text"],
            font=("Poppins", 10, "bold"),
            fg_color=status_info["color"],
            text_color=status_info["text_color"],
            corner_radius=6,
            width=widths[6]
        )
        status_lbl.grid(row=0, column=6, padx=padding, pady=4, sticky="w")

        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=7, padx=padding, pady=4, sticky="e")

        if is_cancelled:
            btn_restore = ctk.CTkButton(
                action_frame,
                text="Aktif Et",
                width=80,
                font=("Poppins", 10, "bold"),
                fg_color="#bfdbfe",
                hover_color="#93c5fd",
                text_color="#0f172a",
                command=lambda rid=res_id: app.reactivate_reservation(rid)
            )
            btn_restore.pack(side="left", padx=4, pady=2)
        elif is_checked_out:
            btn_undo = ctk.CTkButton(
                action_frame,
                text="Aktif Et",
                width=80,
                font=("Poppins", 10, "bold"),
                fg_color="#bfdbfe",
                hover_color="#93c5fd",
                text_color="#0f172a",
                command=lambda rid=res_id: app.undo_checkout(rid)
            )
            btn_undo.pack(side="left", padx=4, pady=2)
        else:
            button_width = 80
            upper_status = (status or "").upper()
            btn_edit = ctk.CTkButton(
                action_frame,
                text="Duzenle",
                width=70,
                font=("Poppins", 10, "bold"),
                fg_color="#cbd5e1",
                hover_color="#94a3b8",
                text_color="#0f172a",
                command=lambda res_tuple=res: app.start_edit_reservation(res_tuple)
            )
            btn_edit.pack(side="left", padx=4, pady=2)
            if upper_status == "CONFIRMED":
                btn_ci = ctk.CTkButton(
                    action_frame,
                    text="Giris Yap",
                    width=button_width,
                    font=("Poppins", 10, "bold"),
                    fg_color="#27ae60",
                    hover_color="#2ecc71",
                    text_color="white",
                    command=lambda rid=res_id: app.handleCheckIn(rid)
                )
                btn_ci.pack(side="left", padx=4, pady=2)
            elif upper_status == "CHECKED_IN":
                btn_co = ctk.CTkButton(
                    action_frame,
                    text="Cikis Yap",
                    width=button_width,
                    font=("Poppins", 10, "bold"),
                    fg_color="#e67e22",
                    hover_color="#f39c12",
                    text_color="white",
                    command=lambda rid=res_id: app.handleCheckOut(rid)
                )
                btn_co.pack(side="left", padx=4, pady=2)

            if upper_status in ["CONFIRMED", "CHECKED_IN"]:
                btn_cancel = ctk.CTkButton(
                    action_frame,
                    text="Iptal",
                    width=70,
                    font=("Poppins", 10, "bold"),
                    fg_color="#c0392b",
                    hover_color="#e74c3c",
                    text_color="white",
                    command=lambda rid=res_id: app.cancel_reservation(rid)
                )
                btn_cancel.pack(side="left", padx=4, pady=2)

    if dataset:
        add_header(app.reservations_scroll, header_title)
        total_sum = 0.0
        for idx, r in enumerate(dataset, start=1):
            add_row(app.reservations_scroll, idx, r, row_state=selected)
            if r[8] is not None:
                total_sum += float(r[8])
        app.label_total_revenue.configure(text=f"Toplam Odeme: {total_sum:.2f} TL")
    else:
        lbl = ctk.CTkLabel(
            app.reservations_scroll,
            text="Bu kategoride rezervasyon yok.",
            font=app.font_normal,
            text_color=app.color_text_main
        )
        lbl.pack(pady=30)
        app.label_total_revenue.configure(text="Toplam Odeme: 0 TL")


def start_edit_reservation(app, res_tuple):
    (
        res_id,
        primary_guest_id,
        room_id,
        guest_names_str,
        room_number,
        ci,
        co,
        status,
        total_amount,
        nightly_price,
        guest_count,
        guest_ids,
        guest_name_list,
    ) = res_tuple

    # Hazir map'ler yoksa olustur
    if not hasattr(app, "guest_choice_map"):
        app.guest_choice_map = {}
    if not hasattr(app, "guest_id_to_label"):
        app.guest_id_to_label = {}

    app.editing_reservation_id = res_id
    app.editing_reservation_status = status

    room_label = f"#{room_number}"
    current_room_values = list(app.combo_res_room.cget("values"))
    app.room_choice_map[room_label] = room_id
    if room_label not in current_room_values:
        app.combo_res_room.configure(values=current_room_values + [room_label])
    app.combo_res_room.set(room_label)
    app.on_room_change(room_label)

    # Misafir listesi ve ID'leri map'le
    labels = []
    if guest_ids and guest_name_list and len(guest_ids) == len(guest_name_list):
        for gid, lbl in zip(guest_ids, guest_name_list):
            if lbl:
                labels.append(lbl)
                app.guest_choice_map[lbl] = gid
                app.guest_id_to_label[gid] = lbl
    else:
        for gid in guest_ids or []:
            lbl = app.guest_id_to_label.get(gid)
            if lbl:
                labels.append(lbl)
                app.guest_choice_map[lbl] = gid
    if not labels and guest_names_str:
        labels = guest_names_str.split(", ")

    # Seçenek listesine olmayan etiketleri ekle
    extra_vals = [l for l in labels if l not in getattr(app, "guest_selector_values", [])]
    if extra_vals:
        app.guest_selector_values = list(app.guest_selector_values) + extra_vals if hasattr(app, "guest_selector_values") else extra_vals
    app.combo_guest_count.set(str(max(1, len(labels))))
    rebuild_guest_selectors(app, max(1, len(labels)), preset_labels=labels)

    app.cb_ci_year.set(f"{ci.year}")
    app.cb_ci_month.set(f"{ci.month:02d}")
    app.cb_ci_day.set(f"{ci.day:02d}")
    app.cb_co_year.set(f"{co.year}")
    app.cb_co_month.set(f"{co.month:02d}")
    app.cb_co_day.set(f"{co.day:02d}")

    app.entry_res_price.delete(0, "end")
    app.entry_res_price.insert(0, str(nightly_price or ""))

    if hasattr(app, "btn_save_res"):
        app.btn_save_res.configure(text="Rezervasyonu Guncelle")

    app.label_res_message.configure(
        text=f"Düzenleme modunda: ID {res_id}",
        text_color="#0ea5e9"
    )


def save_reservation(app):
    guest_labels = [cb.get() for cb in getattr(app, "guest_selectors", [])] if hasattr(app, "guest_selectors") else []
    guest_ids = []
    for lbl in guest_labels:
        gid = app.guest_choice_map.get(lbl)
        if gid:
            guest_ids.append(gid)

    room_label = app.combo_res_room.get() if hasattr(app, "combo_res_room") else ""
    if not guest_ids:
        app.label_res_message.configure(text="Önce misafir seçmelisiniz.", text_color="#dc2626")
        return
    if room_label == "Bos oda yok" or not room_label:
        app.label_res_message.configure(text="Müsait oda bulunamadı.", text_color="#dc2626")
        return

    guest_id_primary = guest_ids[0]
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

    guest_count = len(guest_ids)
    if guest_count <= 0:
        app.label_res_message.configure(text="Kişi sayısı en az 1 olmalı.", text_color="#dc2626")
        return

    capacity = db.get_room_capacity(room_id)
    if capacity is not None and guest_count > capacity:
        app.label_res_message.configure(
            text=f"Bu oda en fazla {capacity} kişi alır.",
            text_color="#dc2626"
        )
        return

    exclude_id = getattr(app, "editing_reservation_id", None)
    if db.room_has_conflict(
        room_id,
        check_in_date,
        check_out_date,
        exclude_reservation_id=exclude_id,
        requested_guest_count=guest_count,
    ):
        app.label_res_message.configure(text="Seçilen tarihlerde bu oda kapasitesi dolu.", text_color="#dc2626")
        return

    if exclude_id:
        ok = db.update_reservation(
            exclude_id,
            guest_id_primary,
            room_id,
            check_in_date,
            check_out_date,
            nightly_price,
            guest_ids=guest_ids,
            status=getattr(app, "editing_reservation_status", "CONFIRMED"),
        )
        if not ok:
            app.label_res_message.configure(text="Rezervasyon güncellenirken hata oluştu.", text_color="#dc2626")
            return
        app.label_res_message.configure(text=f"Rezervasyon güncellendi (ID: {exclude_id}).", text_color="#16a34a")
        reset_edit_mode(app)
    else:
        new_id = db.insert_reservation(
            guest_id_primary,
            room_id,
            check_in_date,
            check_out_date,
            nightly_price,
            guest_ids=guest_ids,
        )
        if new_id is None:
            app.label_res_message.configure(text="Rezervasyon eklenirken hata oluştu.", text_color="#dc2626")
            return
        app.label_res_message.configure(text=f"Rezervasyon oluşturuldu (ID: {new_id})", text_color="#16a34a")

    app.build_reservations_list()
    app.refresh_reservation_choices()
    app.build_room_cards()
    app.refresh_dashboard()


def cancel_reservation(app, reservation_id: int):
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


def reactivate_reservation(app, reservation_id: int):
    ok = db.update_reservation_status(reservation_id, "CONFIRMED")
    if ok:
        app.label_res_message.configure(
            text=f"Rezervasyon yeniden aktif edildi (ID: {reservation_id}).",
            text_color="#16a34a"
        )
        app.build_reservations_list()
        app.refresh_reservation_choices()
        app.build_room_cards()
        app.refresh_dashboard()
    else:
        app.label_res_message.configure(
            text="Rezervasyon yeniden aktif edilirken hata olustu.",
            text_color="#dc2626"
        )


def reset_edit_mode(app):
    app.editing_reservation_id = None
    app.editing_reservation_status = None
    if hasattr(app, "btn_save_res"):
        app.btn_save_res.configure(text="Rezervasyonu Tamamla")
    if hasattr(app, "combo_guest_count"):
        app.combo_guest_count.set("1")
    rebuild_guest_selectors(app, 1)
