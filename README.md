# Görüşme Formu CSV Normalizer

Formidable Forms'dan export edilen **Görüşme ve Gözlem Formu** CSV dosyalarını normalize Excel formatına dönüştürür.

## 🚀 Kullanım

1. [**index.html**](./index.html) dosyasını tarayıcıda açın
2. CSV dosyasını sürükleyip bırakın
3. **Excel Dosyasını İndir** butonuna tıklayın

> Tüm işlemler tarayıcınızda gerçekleşir. Veriler sunucuya gönderilmez.

## 📊 Çıktı Formatı

### Sheet 1: `Sosyal_Sorunlar`
| Sütun | Açıklama |
|-------|----------|
| Sicil No | Personel sicil numarası |
| Aktör ID | Kurum kimliği |
| Üst Grup | Soru kategorisi |
| Alt Grup | Alt soru |
| Değer | Puan (0-5) |

### Sheet 2: `Mahalle_Haritalama`
| Sütun | Açıklama |
|-------|----------|
| Sicil No | Personel sicil numarası |
| Aktör ID | Kurum kimliği |
| İlçe | İlçe adı |
| Üst Grup | Soru kategorisi |
| Alt Grup | Seçilen sorun |
| Mahalle | Tek mahalle (virgülle ayrılanlar bölünür) |

## ⚙️ Dinamik Sütun Desteği

Form genişlese bile çalışır. Sistem **pattern-based sütun tanıma** kullanır:

- `"Soru Metni? - Alt Seçenek"` formatındaki sütunlar otomatik algılanır
- `İlçe Seçiniz` → `Mahalle Seçiniz` → `Seçim Yapınız` üçlüleri otomatik eşleşir

## 🌐 GitHub Pages

Bu repository GitHub Pages ile yayınlanabilir:
1. Settings → Pages → Source: `main` branch
2. URL: `https://[username].github.io/[repo-name]/`

## 📁 Dosyalar

- `index.html` - Web uygulaması
- `csv_to_excel_converter.py` - Python alternatifi (opsiyonel)
