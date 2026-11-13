import tkinter as tk
from tkinter import messagebox
import re

# =========================================================
# ANALİZ MOTORU (REGEX İLE METİN TARAMA)
# =========================================================
def metni_analiz_et(metin):
    riskler = []
    # Tespit edilen verilerin tutulacağı liste
    
    # 1. Telefon Numarası Kontrolü (05XX... formatında 11 hane)
    telefon_deseni = r"0[5][0-9]{9}"
    telefonlar = re.findall(telefon_deseni, metin)
    if telefonlar:
        riskler.append(f"Telefon Numarası ({len(telefonlar)} adet)")

    # 2. E-posta Kontrolü
    eposta_deseni = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    epostalar = re.findall(eposta_deseni, metin)
    if epostalar:
        riskler.append(f"E-posta Adresi ({len(epostalar)} adet)")

    # 3. T.C. Kimlik Numarası Kontrolü (11 haneli ve 0 ile başlamayan)
    tc_deseni = r"[1-9][0-9]{10}"
    tcler = re.findall(tc_deseni, metin)
    if tcler:
        riskler.append(f"T.C. Kimlik Numarası ({len(tcler)} adet)")

    # 4. Adres Bilgisi Kontrolü (Basit Anahtar Kelime)
    adres_kelimeleri = ["mahalle", "sokak", "cadde", "no:", "daire", "apartman", "site"]
    bulunan_adres = [k for k in adres_kelimeleri if k in metin.lower()]
    if bulunan_adres:
        riskler.append("Adres Bilgisi")

    # 5. Okul/Kurum Adı Kontrolü
    okul_kelimeleri = ["lise", "ortaokul", "üniversite", "kolej", "okul"]
    bulunan_okul = [k for k in okul_kelimeleri if k in metin.lower()]
    if bulunan_okul:
        riskler.append("Okul/Kurum Adı")

    return riskler


# =========================================================
# TKINTER ARAYÜZÜ
# =========================================================
def gonderiyi_paylas():
    metin = gonderi_alani.get("1.0", tk.END).strip()
    
    if not metin:
        messagebox.showwarning("Uyarı", "Lütfen paylaşmak istediğiniz bir metin yazın!")
        return

    # Metni analiz et
    riskler = metni_analiz_et(metin)

    # Sonuç kutusunu güncelle
    sonuc_ekrani.config(state="normal")
    sonuc_ekrani.delete("1.0", tk.END)

    if riskler:
        # Risk varsa kırmızı uyarı
        sonuc_ekrani.insert(tk.END, "⚠️ DİKKAT! DİJİTAL AYAK İZİ BIRAKTINIZ!\n", "uyari_baslik")
        sonuc_ekrani.insert(tk.END, "Gönderiniz internete yüklendi ancak şu bilgileri ifşa ettiniz:\n\n", "normal")
        
        for risk in riskler:
            sonuc_ekrani.insert(tk.END, f"• {risk}\n", "riskli")
            
        sonuc_ekrani.insert(tk.END, "\nBu bilgiler kötü niyetli kişiler tarafından toplanarak kimlik hırsızlığında kullanılabilir.", "normal")
        sonuc_ekrani.config(state="disabled")
        
        # Riskli kelimeleri (varsa) ana metin alanında boyamak için (isteğe bağlı ekstra görsellik)
        # Şimdilik sadece sonuç raporunda gösteriyoruz.
        
    else:
        # Risk yoksa yeşil onay
        sonuc_ekrani.insert(tk.END, "✅ GÜVENLİ PAYLAŞIM\n\n", "guvenli_baslik")
        sonuc_ekrani.insert(tk.END, "Tebrikler! Gönderinizde kişisel verilerinizi ifşa edecek bir bilgi bulunamadı. Güvenle paylaşabilirsiniz.", "normal")
        sonuc_ekrani.config(state="disabled")


# --- Ana Pencere ---
root = tk.Tk()
root.title("Dijital Gölge - Dijital Ayak İzi Simülatörü")
root.geometry("750x650")
root.configure(bg="#f4f6f9")

# Başlık
tk.Label(root, text="👤 Dijital Gölge", font=("Arial", 22, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=10)
tk.Label(root, text="Bir gönderi yazın ve 'Paylaş' butonuna basarak dijital ayak izinizi görün.", font=("Arial", 11), bg="#f4f6f9").pack()

# Sosyal Medya Gönderi Alanı (Giriş)
tk.Label(root, text="Gönderinizi buraya yazın (Instagram, Facebook vb.):", font=("Arial", 11, "bold"), bg="#f4f6f9").pack(anchor="w", padx=30, pady=(15, 0))
gonderi_alani = tk.Text(root, height=5, font=("Arial", 12), width=70, bg="white", bd=2, relief="solid")
gonderi_alani.pack(pady=5, padx=30)

# Paylaş Butonu
tk.Button(root, text="📤 Gönderiyi Paylaş", font=("Arial", 13, "bold"), bg="#3498db", fg="white", command=gonderiyi_paylas).pack(pady=15, ipadx=20, ipady=5)

# Sonuç Ekranı
tk.Label(root, text="Analiz Sonucu:", font=("Arial", 11, "bold"), bg="#f4f6f9").pack(anchor="w", padx=30)
sonuc_ekrani = tk.Text(root, height=12, font=("Arial", 12), width=70, bg="#ffffff", bd=2, relief="groove", state="disabled", wrap="word")
sonuc_ekrani.pack(pady=5, padx=30)

# Renk ve Font Etiketleri
sonuc_ekrani.tag_config("uyari_baslik", font=("Arial", 15, "bold"), foreground="#c0392b")
sonuc_ekrani.tag_config("guvenli_baslik", font=("Arial", 15, "bold"), foreground="#27ae60")
sonuc_ekrani.tag_config("riskli", font=("Arial", 12, "bold"), foreground="#c0392b")
sonuc_ekrani.tag_config("normal", font=("Arial", 11), foreground="#333")

root.mainloop()