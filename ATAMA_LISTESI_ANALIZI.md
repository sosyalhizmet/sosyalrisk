# 📊 atama_listesi.xlsx Veri Analizi

*Analiz Tarihi: 2026-01-17*

---

## 📑 Dosya Yapısı

| Özellik | Değer |
|---------|-------|
| **Dosya Adı** | atama_listesi.xlsx |
| **Sayfalar** | Adresler, Sayfa2 |
| **Toplam Satır** | 4.309 kayıt |
| **Sütun Sayısı** | 13 |

---

## 📋 Sütun Yapısı (Adresler Sayfası)

| # | Sütun Adı | Veri Tipi | Açıklama |
|---|-----------|-----------|----------|
| 1 | `ID` | Sayısal | Benzersiz kayıt numarası |
| 2 | `ADI` | Metin | Kurum/hizmet adı |
| 3 | `ANA KATEGORİ` | Kategorik | Kurum tipi |
| 4 | `ALT KATEGORI` | Kategorik | Hizmet türü (221 farklı değer) |
| 5 | `ÇALIŞMA ALANI` | Kategorik | Faaliyet alanı |
| 6 | `DEZAVANTAJLI GRUP` | Kategorik | Hedef kitle |
| 7 | `ILCE` | Metin | İlçe adı |
| 8 | `ILCE_UAVT` | Sayısal | İlçe UAVT kodu |
| 9 | `MAHALLE` | Metin | Mahalle adı |
| 10 | `MAHALLE_UAVT` | Sayısal | Mahalle UAVT kodu |
| 11 | `ADRES` | Metin | Tam adres |
| 12 | `KOORDİNATLAR` | Metin | Lat, Long (örn: "40.920272, 29.186948") |
| 13 | `Atama Durumu` | Kategorik | Evet / Hayır / Boş |

---

## 📈 Değer Dağılımları

### Ana Kategoriler (9 benzersiz değer)

| Kategori | Not |
|----------|-----|
| İLÇE BELEDİYELERİ | Büyük harf |
| İlçe Belediyeleri | Küçük harf (tutarsızlık) |
| KAMU | - |
| Kamu | Küçük harf (tutarsızlık) |
| ÖZEL | - |
| Özel | Küçük harf (tutarsızlık) |
| STÖ | Sivil Toplum Örgütü |
| SHDB | Sosyal Hizmetler Daire Başkanlığı |
| İBB | İstanbul Büyükşehir Belediyesi |

---

### Dezavantajlı Gruplar (18 benzersiz değer)

| Grup | Alternatif Yazım |
|------|------------------|
| ÇOCUK | Çocuk |
| KADIN | Kadın |
| ENGELLİ | Engelli |
| YAŞLI | Yaşlı |
| GENÇ | Genç |
| GÖÇMEN | Göçmen |
| ROMAN | Roman |
| EVSİZ | - |
| LGBTİ | - |
| GENEL | Genel |

> ⚠️ **Not:** Büyük/küçük harf tutarsızlığı mevcut. Normalize edilmeli.

---

### Çalışma Alanları (31 benzersiz değer)

| Alan | Açıklama |
|------|----------|
| GÜNDÜZLÜ BAKIM | Kreş, gündüz bakımevi |
| EĞİTİM / Eğitim | Eğitim kurumları |
| SAĞLIK / Sağlık | Sağlık hizmetleri |
| SOSYAL HİZMET / Sosyal Hizmet | Sosyal destek |
| BAKIM | Bakım hizmetleri |
| BARINMA | Barınma desteği |
| KÜLTÜR VE SANAT | Kültürel faaliyetler |
| SPOR | Spor tesisleri |
| DANIŞMA | Danışmanlık hizmetleri |
| HAK ODAKLI | Hak temelli çalışmalar |
| GÜVENLİK | Güvenlik hizmetleri |
| ÇEVRE VE AFET | Çevre ve afet yönetimi |
| ÇALIŞMA HAYATI | İstihdam desteği |
| ÖZ ÖRGÜTLENME | Topluluk örgütlenmesi |
| İNANÇ | Dini kurumlar |
| YEREL | Yerel hizmetler |
| GENEL | Genel hizmetler |

---

### İlçe Dağılımı (29 benzersiz değer)

```
Arnavutköy, Ataşehir, Avcılar, Bahçelievler, Bakırköy, 
Başakşehir, Beşiktaş, Beykoz, Beyoğlu, Çatalca, 
Çekmeköy, Fatih, Gaziosmanpaşa, Güngören, Kadıköy, 
Kağıthane, Kartal, Küçükçekmece, Maltepe, Pendik, 
Sancaktepe, Sarıyer, Sultanbeyli, Şişli, Tuzla, 
Ümraniye, Zeytinburnu, Firuzağa*
```

> ⚠️ **Not:** "Kartal" ve "KARTAL" gibi büyük/küçük harf tutarsızlıkları var.
> ⚠️ **Not:** "Firuzağa" bir mahalle, ilçe olarak yanlış girilmiş olabilir.

---

### Atama Durumu

| Değer | Açıklama |
|-------|----------|
| `Evet` | Atama yapılmış |
| `Hayır` | Atama yapılmamış |
| `undefined` (boş) | Henüz belirlenmemiş |

---

## ⚠️ Veri Kalitesi Sorunları

### 1. Büyük/Küçük Harf Tutarsızlığı
- "KADIN" vs "Kadın"
- "KARTAL" vs "Kartal"
- "KAMU" vs "Kamu"

**Çözüm:** Tüm kategorik değerleri normalize etmek için `toUpperCase()` veya mapping kullanılmalı.

### 2. Çok Sayıda Alt Kategori
- 221 farklı alt kategori mevcut
- Bazıları çok spesifik, gruplanabilir

### 3. Eksik Veriler
- `Atama Durumu` sütununda çoğu kayıt boş
- Bazı kayıtlarda `ÇALIŞMA ALANI` eksik

### 4. Koordinat Formatı
- Format: "lat, long" (metin olarak)
- Harita için parse edilmeli

---

## 🔗 Örnek Kayıt

```json
{
  "ID": 10459005,
  "ADI": "KARTAL BELEDİYESİ SOĞANLIK ÇOCUK GELİŞİM MERKEZİ",
  "ANA KATEGORİ": "İLÇE BELEDİYELERİ",
  "ALT KATEGORI": "KREŞ/GÜNDÜZ BAKIMEVİ",
  "ÇALIŞMA ALANI": "GÜNDÜZLÜ BAKIM",
  "DEZAVANTAJLI GRUP": "ÇOCUK",
  "ILCE": "KARTAL",
  "ILCE_UAVT": 34776,
  "MAHALLE": "SOĞANLIK YENİ",
  "MAHALLE_UAVT": 28453,
  "ADRES": "Soğanlık Yeni Mah. ... Kartal/İstanbul",
  "KOORDİNATLAR": "40.920272, 29.186948",
  "Atama Durumu": undefined
}
```

---

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam Kayıt | 4.309 |
| Benzersiz Ana Kategori | 9 |
| Benzersiz Alt Kategori | 221 |
| Benzersiz Çalışma Alanı | 31 |
| Benzersiz Dezavantajlı Grup | 18 |
| Benzersiz İlçe | 29 |

---

## 💡 Kullanım Önerileri

1. **Harita Görselleştirmesi:** Koordinatlar mevcut, Leaflet.js ile gösterilebilir
2. **Filtreleme Aracı:** Ana kategori, ilçe, dezavantajlı gruba göre filtre
3. **Atama Takibi:** Atama durumu sütunu ile takip sistemi
4. **Veri Temizliği:** Büyük/küçük harf normalizasyonu gerekli

---

*Bu analiz sosyalrisk sistemi için hazırlanmıştır.*
