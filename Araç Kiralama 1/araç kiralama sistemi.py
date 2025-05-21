
import tkinter as tk
from tkinter import messagebox
# ---------------- Sınıflar ---------------- #
class Arac:
    def __init__(self, arac_id, model, kiralama_durumu=False):
        self.arac_id = arac_id
        self.model = model
        self.kiralama_durumu = kiralama_durumu

    def arac_durumu_guncelle(self, durum):
        self.kiralama_durumu = durum

class Musteri:
    def __init__(self, musteri_id, ad, soyad):
        self.musteri_id = musteri_id
        self.ad = ad
        self.soyad = soyad

class Kiralama:
    def __init__(self):
        self.kiralamalar = []

    def kiralama_yap(self, musteri, arac):
        if not arac.kiralama_durumu:
            arac.kiralama_durumu = True
            self.kiralamalar.append({'musteri': musteri, 'arac': arac})
            return True
        return False

    def kiralama_bilgisi(self):
        bilgiler = []
        for kira in self.kiralamalar:
            m = kira['musteri']
            a = kira['arac']
            bilgiler.append(f"{m.ad} {m.soyad} - {a.model}")
        return bilgiler

# ---------------- Veriler ---------------- #

arac_listesi = []
musteri_listesi = []
kiralama_yonetimi = Kiralama()

# ---------------- GUI Arayüz ---------------- #

def arayuz_olustur():
    pencere = tk.Tk()
    pencere.title("Araç Kiralama Sistemi")

    # Araç Ekleme
    def arac_ekle():
        aid = entry_arac_id.get()
        model = entry_arac_model.get()
        if aid and model:
            arac_listesi.append(Arac(aid, model))
            messagebox.showinfo("Başarılı", "Araç eklendi!")
            entry_arac_id.delete(0, tk.END)
            entry_arac_model.delete(0, tk.END)

    # Müşteri Ekleme
    def musteri_ekle():
        mid = entry_musteri_id.get()
        ad = entry_musteri_ad.get()
        soyad = entry_musteri_soyad.get()
        if mid and ad and soyad:
            musteri_listesi.append(Musteri(mid, ad, soyad))
            messagebox.showinfo("Başarılı", "Müşteri eklendi!")
            entry_musteri_id.delete(0, tk.END)
            entry_musteri_ad.delete(0, tk.END)
            entry_musteri_soyad.delete(0, tk.END)

    # Kiralama Yapma
    def kiralama_yap():
        try:
            musteri = musteri_listesi[listbox_musteriler.curselection()[0]]
            arac = arac_listesi[listbox_araclar.curselection()[0]]
            if kiralama_yonetimi.kiralama_yap(musteri, arac):
                messagebox.showinfo("Başarılı", f"{arac.model} aracı kiralandı.")
                guncelle_arac_listesi()
            else:
                messagebox.showwarning("Uyarı", "Araç zaten kiralanmış.")
        except IndexError:
            messagebox.showerror("Hata", "Lütfen müşteri ve araç seçin.")

    # Kiralama Bilgilerini Göster
    def kiralama_goster():
        bilgiler = kiralama_yonetimi.kiralama_bilgisi()
        text_kiralamalar.delete("1.0", tk.END)
        if bilgiler:
            text_kiralamalar.insert(tk.END, "\n".join(bilgiler))
        else:
            text_kiralamalar.insert(tk.END, "Henüz kiralama yok.")

    def guncelle_arac_listesi():
        listbox_araclar.delete(0, tk.END)
        for a in arac_listesi:
            durum = "Kirada" if a.kiralama_durumu else "Uygun"
            listbox_araclar.insert(tk.END, f"{a.model} ({durum})")

    def guncelle_musteri_listesi():
        listbox_musteriler.delete(0, tk.END)
        for m in musteri_listesi:
            listbox_musteriler.insert(tk.END, f"{m.ad} {m.soyad}")

    # --- Layout --- #

    # Araç Ekleme Alanı
    tk.Label(pencere, text="Araç ID").grid(row=0, column=0)
    entry_arac_id = tk.Entry(pencere)
    entry_arac_id.grid(row=0, column=1)

    tk.Label(pencere, text="Araç Model").grid(row=1, column=0)
    entry_arac_model = tk.Entry(pencere)
    entry_arac_model.grid(row=1, column=1)

    tk.Button(pencere, text="Araç Ekle", command=lambda: [arac_ekle(), guncelle_arac_listesi()]).grid(row=2, column=1)

    # Müşteri Ekleme Alanı
    tk.Label(pencere, text="Müşteri ID").grid(row=3, column=0)
    entry_musteri_id = tk.Entry(pencere)
    entry_musteri_id.grid(row=3, column=1)

    tk.Label(pencere, text="Ad").grid(row=4, column=0)
    entry_musteri_ad = tk.Entry(pencere)
    entry_musteri_ad.grid(row=4, column=1)

    tk.Label(pencere, text="Soyad").grid(row=5, column=0)
    entry_musteri_soyad = tk.Entry(pencere)
    entry_musteri_soyad.grid(row=5, column=1)

    tk.Button(pencere, text="Müşteri Ekle", command=lambda: [musteri_ekle(), guncelle_musteri_listesi()]).grid(row=6, column=1)

    # Araç ve Müşteri Listeleri
    tk.Label(pencere, text="Araçlar").grid(row=0, column=2)
    listbox_araclar = tk.Listbox(pencere, width=30)
    listbox_araclar.grid(row=1, column=2, rowspan=5)

    tk.Label(pencere, text="Müşteriler").grid(row=0, column=3)
    listbox_musteriler = tk.Listbox(pencere, width=30)
    listbox_musteriler.grid(row=1, column=3, rowspan=5)

    # Kiralama Butonu
    tk.Button(pencere, text="Araç Kirala", command=kiralama_yap).grid(row=6, column=2)

    # Kiralama Bilgileri Göster
    tk.Button(pencere, text="Kiralama Bilgileri", command=kiralama_goster).grid(row=6, column=3)
    text_kiralamalar = tk.Text(pencere, height=8, width=60)
    text_kiralamalar.grid(row=7, column=0, columnspan=4, pady=10)

    pencere.mainloop()

if __name__ == "__main__":
    arayuz_olustur()
