import imaplib
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import messagebox
import threading

# GPIO modunu ve pin numarasını ayarlayın
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
YESIL_LED = 22
KIRMIZI_LED = 24
GPIO.setup(YESIL_LED, GPIO.OUT)
GPIO.setup(KIRMIZI_LED, GPIO.OUT)

# LED'leri varsayılan olarak kapat
GPIO.output(YESIL_LED, False)
GPIO.output(KIRMIZI_LED, False)

# Outlook IMAP hesap bilgilerini varsayılan değerlerle ayarlayın
email_address = ""  # e-posta adresi
password = ""  # Outlook hesabınızın şifresi

# Varsayılan LED sürelerini ve e-posta kontrol süresini ayarlayın (saniye cinsinden)
default_green_led_time = 5
default_red_led_time = 2
default_email_check_interval = 15

def check_new_emails():
    try:
        # Outlook IMAP sunucusuna bağlanma
        mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")

        # Giriş yapma
        mail.login(email_address, password)

        # Gelen kutusuna erişim
        mail.select("inbox")

        # Yeni e-posta kontrolü yapma
        status, messages = mail.search(None, "UNSEEN")

        # Yeni e-posta geldiyse yeşil LED'i aç
        if status == "OK" and messages[0]:
            return True
        else:
            return False

    except Exception as e:
        print("E-posta kontrolü yapılırken bir hata oluştu:", e)
        return False

def save_settings_to_file(green_led_time, red_led_time, email_check_interval):
    with open("settings.txt", "w") as file:
        file.write(f"{email_address}\n{password}\n{green_led_time}\n{red_led_time}\n{email_check_interval}")

def load_settings_from_file():
    try:
        with open("settings.txt", "r") as file:
            global email_address, password, default_green_led_time, default_red_led_time, default_email_check_interval
            lines = file.readlines()
            if len(lines) >= 5:
                email_address = lines[0].strip()
                password = lines[1].strip()
                default_green_led_time = int(lines[2].strip())
                default_red_led_time = int(lines[3].strip())
                default_email_check_interval = int(lines[4].strip())
            else:
                print("Dosya içeriği eksik veya hatalı.")
    except FileNotFoundError:
        # Eğer dosya yoksa veya hatalıysa varsayılan değerleri kullanmaya devam edelim
        pass

def main_loop():
    try:
        while True:
            # Yeni e-posta kontrolü yap
            new_email = check_new_emails()

            if new_email:
                print("ÇAĞRI VAR!")
                GPIO.output(KIRMIZI_LED, False)  # Kırmızı LED'i söndür
                GPIO.output(YESIL_LED, True)  # Yeşil LED'i aç
                time.sleep(default_green_led_time)
                GPIO.output(YESIL_LED, False)  # Yeşil LED'i söndür
            else:
                print("ÇAĞRI YOK!")
                GPIO.output(YESIL_LED, False)  # Yeşil LED'i söndür
                GPIO.output(KIRMIZI_LED, True)  # Kırmızı LED'i aç
                time.sleep(default_red_led_time)

            # Kontrol aralığını ayarlayın
            time.sleep(default_email_check_interval)

    except KeyboardInterrupt:
        GPIO.cleanup()

def run_gui():
    def update_settings():
        global email_address, password, default_green_led_time, default_red_led_time, default_email_check_interval
        email_address = email_entry.get()
        password = password_entry.get()
        default_green_led_time = int(green_led_entry.get())
        default_red_led_time = int(red_led_entry.get())
        default_email_check_interval = int(email_check_interval_entry.get())
        save_settings_to_file(default_green_led_time, default_red_led_time, default_email_check_interval)
        messagebox.showinfo("Bilgi", "Ayarlar kaydedildi!")

    load_settings_from_file()

    root = tk.Tk()
    root.title("E-posta Bildirim ve Kontrol Uygulaması")

    # E-posta ayarları başlık
    email_settings_label = tk.Label(root, text="E-posta Ayarları", font=("Arial", 16))
    email_settings_label.grid(row=0, column=0, columnspan=2, pady=10)

    # E-posta adresi ve şifre girişleri
    email_label = tk.Label(root, text="E-posta Adresi:")
    email_label.grid(row=1, column=0)
    email_entry = tk.Entry(root)
    email_entry.grid(row=1, column=1)
    email_entry.insert(0, email_address)

    password_label = tk.Label(root, text="Şifre:")
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=2, column=1)
    password_entry.insert(0, password)

    # LED ayarları başlık
    led_settings_label = tk.Label(root, text="LED Ayarları", font=("Arial", 16))
    led_settings_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Yeşil LED süresi girişi
    green_led_label = tk.Label(root, text="Yeşil LED Süresi (saniye):")
    green_led_label.grid(row=4, column=0)
    green_led_entry = tk.Entry(root)
    green_led_entry.grid(row=4, column=1)
    green_led_entry.insert(0, default_green_led_time)

    # Kırmızı LED süresi girişi
    red_led_label = tk.Label(root, text="Kırmızı LED Süresi (saniye):")
    red_led_label.grid(row=5, column=0)
    red_led_entry = tk.Entry(root)
    red_led_entry.grid(row=5, column=1)
    red_led_entry.insert(0, default_red_led_time)

    # E-posta kontrol süresi girişi
    email_check_interval_label = tk.Label(root, text="E-posta Kontrol Süresi (saniye):")
    email_check_interval_label.grid(row=6, column=0)
    email_check_interval_entry = tk.Entry(root)
    email_check_interval_entry.grid(row=6, column=1)
    email_check_interval_entry.insert(0, default_email_check_interval)

    # Ayarları kaydet butonu
    save_button = tk.Button(root, text="Ayarları Kaydet", command=update_settings)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.daemon = True
    main_thread.start()

    run_gui()

