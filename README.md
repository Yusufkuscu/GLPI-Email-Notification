# GLPI E-posta Bildirim Uygulaması 🚀

## Proje Açıklaması 📝

Bu proje, staj sürecim boyunca geliştirdiğim bir uygulamadır. GLPI (Gestion Libre de Parc Informatique) sistemindeki çağrıları e-posta aracılığıyla çekerek fiziksel LED'lere bildirim olarak dönüştürmeyi amaçlamaktadır.

## Nasıl Çalıştırılır 🛠️

1. Projenin ana dizininde bulunan `GLPI_Emaıl_Notification.py` dosyasını çalıştırın.

2. Uygulama başladığında, e-posta adresinizi ve şifrenizi girmeniz için bir pencere açılacaktır.

3. E-posta ayarlarınızı girdikten sonra "Ayarları Kaydet" düğmesine tıklayın.

4. Uygulamayı başlatın ve GLPI sistemine giriş yapın.

5. GLPI sistemine yeni bir çağrı eklendiğinde, uygulama otomatik olarak bu çağrıyı e-posta yoluyla kontrol edecek ve eğer çağrı varsa yeşil LED yanacak, yoksa kırmızı LED yanacak.

![Yeşil LED](https://github.com/Yusufkuscu/GLPI-Email-Notification/assets/99915079/7245229e-4dbb-4e74-a402-bb24ad4e3c83)
![Kırmızı LED](https://github.com/Yusufkuscu/GLPI-Email-Notification/assets/99915079/cff24671-f2ab-4829-b1ad-faa960438a35)


## Kullanılan Teknolojiler 💻

- Python: Uygulama, Python programlama dili ile geliştirilmiştir.
- Tkinter: Arayüz için Tkinter kütüphanesi kullanılmıştır.
- IMAP ve SMTP: E-posta işlemleri için IMAP ve SMTP protokolleri kullanılmıştır.

## Proje Görüntüleri 📷

![Arayüz](https://github.com/Yusufkuscu/GLPI-Email-Notification/assets/99915079/5884cd50-32cf-4a06-9f5e-c41e06d3fe2e)
