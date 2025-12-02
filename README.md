# Hotel Management System

Bu proje, otel yönetimi için geliştirilmiş bir masaüstü uygulamasıdır.  
Oda yönetimi, rezervasyon işlemleri, misafir bilgileri ve oda türleri gibi temel operasyonları içerir.

---

## 🚀 Özellikler

- Oda ekleme, silme, güncelleme
- Oda türü yönetimi
- Misafir ekleme ve listeleme
- Rezervasyon oluşturma ve yönetme
- Dashboard ekranı
- Modern CustomTkinter arayüzü
- Modüler klasör yapısı
- Backend servis bağlantısı

---

🔧 Gereksinimler
Aşağıdaki Python paketleri gereklidir:

pip install customtkinter
pip install pillow
pip install tk

Eğer PostgreSQL kullanıyorsanız:

pip install psycopg2

▶️ Uygulamayı Çalıştırma

python app.py

Eğer bir sanal ortam kullanıyorsanız:

venv\Scripts\activate
python app.py

🧩 Kullanılan Teknolojiler

Python 3.10+

CustomTkinter – modern UI bileşenleri

Tkinter – temel arayüz kütüphanesi

PostgreSQL (opsiyonel)

Backend Service Layer (hotel_service)

📷 Ekran Görüntüleri

<img width="1918" height="1017" alt="Ekran görüntüsü 2025-12-02 210834" src="https://github.com/user-attachments/assets/10aa3b55-f47a-465b-8558-4feb633df01c" />
<img width="1912" height="1017" alt="Ekran görüntüsü 2025-12-02 211009" src="https://github.com/user-attachments/assets/19f37127-4d31-43be-9416-c6b51b453417" />
<img width="1903" height="1007" alt="Ekran görüntüsü 2025-12-02 210944" src="https://github.com/user-attachments/assets/acb2e599-e204-4d79-9ad8-89cba030b812" />
<img width="1919" height="1019" alt="Ekran görüntüsü 2025-12-02 210915" src="https://github.com/user-attachments/assets/9f2e664e-3595-4e35-9584-48c8beabfa6a" />
<img width="1919" height="1017" alt="Ekran görüntüsü 2025-12-02 210855" src="https://github.com/user-attachments/assets/e7e177f7-ab4e-45b4-882d-f0f3b6b5d574" />

## 📁 Proje Yapısı

```plaintext
project/
│
├── backend/
│   ├── services/
│   │   └── hotel_service.py
│   └── database.py
│
├── frontend/
│   ├── views/
│   │   ├── dashboard_view.py
│   │   ├── reservations_view.py
│   │   ├── rooms_view.py
│   │   ├── room_types_view.py
│   │   └── guests_view.py
│   └── theme.py
│
└── app.py

