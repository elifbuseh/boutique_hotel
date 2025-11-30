import tkinter as tk
import customtkinter as ctk
from backend.services import hotel_service as db
import calendar
from datetime import datetime
import sys, traceback
import tkinter.messagebox as mb # Hata mesajları için (opsiyonel)

# React kartlarına karşılık gelen renkler ve ikonlar
CARD_DATA = [
    {"title": "Toplam Oda", "icon": "🏠", "color": "#2ecc71", "text_color": "#004d26"},
    {"title": "Yeni Rezervasyon", "icon": "🗓️", "color": "#3498db", "text_color": "#084166"},
    {"title": "Aktif Misafirler", "icon": "👥", "color": "#9b59b6", "text_color": "#3f1b53"},
    {"title": "Doluluk Oranı", "icon": "⭐️", "color": "#e74c3c", "text_color": "#5e1c18"},
]

def create_dashboard_frame(app, parent):
    frame = ctk.CTkFrame(parent, corner_radius=24, fg_color=app.color_card)

    # Başlık Alanı
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(pady=(20, 10), anchor="w", padx=25)

    title = ctk.CTkLabel(
        header_frame,
        text="Genel Bakış",
        font=app.font_title,
        text_color="#2c3e50"
    )
    title.pack(side="left", padx=(0, 10))

    subtitle = ctk.CTkLabel(
        header_frame,
        text="| Bugünün Raporu",
        font=app.font_subtitle,
        text_color="#95a5a6"
    )
    subtitle.pack(side="left", pady=(5, 0))

    # Kartlar Alanı
    cards_frame = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0)
    cards_frame.pack(fill="x", padx=20, pady=(5, 10))
    
    # Her bir kartı oluştur ve referanslarını kaydet
    app.lbl_stat_total_rooms = _create_stat_card(app, cards_frame, 0, CARD_DATA[0])
    app.lbl_stat_month_res = _create_stat_card(app, cards_frame, 1, CARD_DATA[1])
    app.lbl_stat_active_guests = _create_stat_card(app, cards_frame, 2, CARD_DATA[2])
    app.lbl_stat_occupancy = _create_stat_card(app, cards_frame, 3, CARD_DATA[3])

    # Grafik Alanı
    chart_container = ctk.CTkFrame(frame, fg_color=app.color_card, corner_radius=16)
    chart_container.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    chart_title = ctk.CTkLabel(
        chart_container,
        text="Yıllık Rezervasyon Analizi (2025)",
        font=("Poppins", 14, "bold"),
        text_color="#2c3e50"
    )
    chart_title.pack(anchor="w", padx=15, pady=(15, 5))
    
    # Grafik Çizim Alanı (Canvas)
    app.dashboard_chart_canvas = tk.Canvas(
        chart_container,
        bg=app.color_card,
        highlightthickness=0
    )
    app.dashboard_chart_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    
    # Canvas resize olayını bağla
    app.dashboard_chart_canvas.bind("<Configure>", lambda event: refresh_dashboard(app))

    # Grafik alt metni
    chart_footer = ctk.CTkLabel(
        chart_container,
        text="Bu grafik, mevcut yıldaki aylık toplam rezervasyon sayılarını göstermektedir.",
        font=("Poppins", 10),
        text_color="#888"
    )
    chart_footer.pack(anchor="center", pady=(0, 10))

    return frame


def _create_stat_card(app, parent, col, data):
    card = ctk.CTkFrame(
        parent, 
        fg_color=data["color"], 
        corner_radius=16, 
        height=140
    )
    card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
    parent.grid_columnconfigure(col, weight=1)

    inner_frame = ctk.CTkFrame(card, fg_color="transparent")
    inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    lbl_icon = ctk.CTkLabel(
        inner_frame,
        text=data["icon"],
        font=("Poppins", 40),
        text_color=data["text_color"]
    )
    lbl_icon.pack(side="left", anchor="nw")

    value_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
    value_frame.pack(side="right", anchor="ne")

    lbl_title = ctk.CTkLabel(
        value_frame,
        text=data["title"],
        font=app.font_subtitle,
        text_color="#fff",
        anchor="e"
    )
    lbl_title.pack(anchor="e", padx=0, pady=(0, 0))

    lbl_value = ctk.CTkLabel(
        value_frame,
        text="0", # Başlangıç değeri
        font=("Poppins", 32, "bold"),
        text_color="#fff",
        anchor="e"
    )
    lbl_value.pack(anchor="e", padx=0, pady=(4, 0))

    return lbl_value


def _draw_chart(app, data):
    """Grafik çizimini gerçekleştirir."""
    canvas = app.dashboard_chart_canvas
    canvas.delete("all")

    # Canvas boyutunu al, ilk çalıştırmada 0 gelme ihtimaline karşı kontrol
    width = canvas.winfo_width() if canvas.winfo_width() > 50 else 800
    height = canvas.winfo_height() if canvas.winfo_height() > 50 else 300
    
    margin = 40
    
    month_to_count = {m: c for (m, c) in data}
    yearly_counts = [month_to_count.get(i + 1, 0) for i in range(12)]
    
    max_count = max(yearly_counts) if yearly_counts else 1
    if max_count == 0:
        max_count = 1

    bar_space = (width - 2 * margin)
    bar_width = (bar_space / 12)
    bar_padding = 10 
    chart_bar_color = "#3498db"
    months_abbr = list(calendar.month_abbr)[1:]
    
    # Y Ekseni (Referans Çizgisi)
    canvas.create_line(margin, height - margin, width - margin / 2, height - margin, fill="#ccc", width=1)

    for i in range(12):
        month_label = months_abbr[i]
        count = yearly_counts[i]
        
        x0 = margin + i * bar_width + bar_padding / 2
        x1 = x0 + bar_width - bar_padding
        
        graph_height = height - 2 * margin
        bar_height = graph_height * (count / max_count)
        
        y1 = height - margin
        y0 = y1 - bar_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=chart_bar_color, width=0)
        
        if count > 0:
            canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(count),
                                 fill="#3498db", font=("Poppins", 11, "bold"))

        canvas.create_text((x0 + x1) / 2, height - margin + 12, text=month_label,
                             fill="#374151", font=("Poppins", 10))

    # Y ekseni maks ve min etiketleri
    canvas.create_text(margin - 15, margin + 5, text=str(max_count), fill="#374151", font=("Poppins", 9))
    canvas.create_text(margin - 15, height - margin, text="0", fill="#374151", font=("Poppins", 9))


def refresh_dashboard(app):
    """Dashboard verilerini veritabanından çeker ve kartları/grafiği günceller."""
    try:
        # 1. Stat Kartları Verisi
        # ÖNEMLİ KONTROL: db.get_dashboard_stats() 4 değer döndürmelidir.
        total_rooms, res_this_month, active_guests, occ_rate = db.get_dashboard_stats()

        # Stat kartlarını güncelle
        app.lbl_stat_total_rooms.configure(text=str(total_rooms))
        app.lbl_stat_month_res.configure(text=str(res_this_month))
        app.lbl_stat_active_guests.configure(text=str(active_guests))
        app.lbl_stat_occupancy.configure(text=f"%{int(occ_rate * 100)}")

        # 2. Grafik Verisi
        data = db.get_yearly_reservation_stats()
        _draw_chart(app, data)
        
    except Exception as e:
        # Veritabanı sorgusu veya bağlantısı hatası burada yakalanır.
        # Bu, en kritik sorundur ve DB'deki metotlarınızda (hotel_service.py) düzeltilmelidir.
        print(f"HATA! Dashboard verileri çekilemedi. Lütfen DB sorgularını kontrol edin: {e}")
        # Kartları hata mesajıyla güncelle
        app.lbl_stat_total_rooms.configure(text="N/A")
        app.lbl_stat_month_res.configure(text="HATA")
        app.lbl_stat_active_guests.configure(text="N/A")
        app.lbl_stat_occupancy.configure(text="N/A")
        
        # Boş grafik çizimi (hatayı göstermek için)
        _draw_chart(app, [])