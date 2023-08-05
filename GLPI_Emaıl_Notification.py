import imaplib
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import messagebox
import threading

# GPIO modunu ve pin numaras�n� ayarlay�n
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
YESIL_LED = 22
KIRMIZI_LED = 24
GPIO.setup(YESIL_LED, GPIO.OUT)
GPIO.setup(KIRMIZI_LED, GPIO.OUT)

# LED'leri varsay�lan olarak kapat
GPIO.output(YESIL_LED, False)
GPIO.output(KIRMIZI_LED, False)

# Outlook IMAP hesap bilgilerini varsay�lan de�erlerle ayarlay�n
email_address = ""  # e-posta adresi
password = ""  # Outlook hesab�n�z�n �ifresi

# Varsay�lan LED s�relerini ve e-posta kontrol s�resini ayarlay�n (saniye cinsinden)
default_green_led_time = 5
default_red_led_time = 2
default_email_check_interval = 15

def check_new_emails():
    try:
        # Outlook IMAP sunucusuna ba�lanma
        mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")

        # Giri� yapma
        mail.login(email_address, password)

        # Gelen kutusuna eri�im
        mail.select("inbox")

        # Yeni e-posta kontrol� yapma
        status, messages = mail.search(None, "UNSEEN")

        # Yeni e-posta geldiyse ye�il LED'i a�
        if status == "OK" and messages[0]:
            return True
        else:
            return False

    except Exception as e:
        print("E-posta kontrol� yap�l�rken bir hata olu�tu:", e)
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
                print("Dosya i�eri�i eksik veya hatal�.")
    except FileNotFoundError:
        # E�er dosya yoksa veya hatal�ysa varsay�lan de�erleri kullanmaya devam edelim
        pass

def main_loop():
    try:
        while True:
            # Yeni e-posta kontrol� yap
            new_email = check_new_emails()

            if new_email:
                print("�A�RI VAR!")
                GPIO.output(KIRMIZI_LED, False)  # K�rm�z� LED'i s�nd�r
                GPIO.output(YESIL_LED, True)  # Ye�il LED'i a�
                time.sleep(default_green_led_time)
                GPIO.output(YESIL_LED, False)  # Ye�il LED'i s�nd�r
            else:
                print("�A�RI YOK!")
                GPIO.output(YESIL_LED, False)  # Ye�il LED'i s�nd�r
                GPIO.output(KIRMIZI_LED, True)  # K�rm�z� LED'i a�
                time.sleep(default_red_led_time)

            # Kontrol aral���n� ayarlay�n
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
    root.title("E-posta Bildirim ve Kontrol Uygulamas�")

    # E-posta ayarlar� ba�l�k
    email_settings_label = tk.Label(root, text="E-posta Ayarlar�", font=("Arial", 16))
    email_settings_label.grid(row=0, column=0, columnspan=2, pady=10)

    # E-posta adresi ve �ifre giri�leri
    email_label = tk.Label(root, text="E-posta Adresi:")
    email_label.grid(row=1, column=0)
    email_entry = tk.Entry(root)
    email_entry.grid(row=1, column=1)
    email_entry.insert(0, email_address)

    password_label = tk.Label(root, text="�ifre:")
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=2, column=1)
    password_entry.insert(0, password)

    # LED ayarlar� ba�l�k
    led_settings_label = tk.Label(root, text="LED Ayarlar�", font=("Arial", 16))
    led_settings_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Ye�il LED s�resi giri�i
    green_led_label = tk.Label(root, text="Ye�il LED S�resi (saniye):")
    green_led_label.grid(row=4, column=0)
    green_led_entry = tk.Entry(root)
    green_led_entry.grid(row=4, column=1)
    green_led_entry.insert(0, default_green_led_time)

    # K�rm�z� LED s�resi giri�i
    red_led_label = tk.Label(root, text="K�rm�z� LED S�resi (saniye):")
    red_led_label.grid(row=5, column=0)
    red_led_entry = tk.Entry(root)
    red_led_entry.grid(row=5, column=1)
    red_led_entry.insert(0, default_red_led_time)

    # E-posta kontrol s�resi giri�i
    email_check_interval_label = tk.Label(root, text="E-posta Kontrol S�resi (saniye):")
    email_check_interval_label.grid(row=6, column=0)
    email_check_interval_entry = tk.Entry(root)
    email_check_interval_entry.grid(row=6, column=1)
    email_check_interval_entry.insert(0, default_email_check_interval)

    # Ayarlar� kaydet butonu
    save_button = tk.Button(root, text="Ayarlar� Kaydet", command=update_settings)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.daemon = True
    main_thread.start()

    run_gui()

    fsafs