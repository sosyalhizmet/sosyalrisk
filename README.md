# İstanbul Sosyal Harita

İstanbul genelinde sosyal sorunların ilçe ve mahalle bazında görselleştirilmesi.

## 🚀 Başlangıç

1. Projeyi klonlayın
2. Herhangi bir HTTP sunucu ile çalıştırın:
   ```bash
   npx serve .
   ```
3. Tarayıcıda [http://localhost:3000](http://localhost:3000) adresini açın

## 📁 Dosya Yapısı

```
istanbul-sosyal-harita/
├── index.html              # Ana sayfa
├── istanbul_harita_v2.html # Harita uygulaması
├── nufus_metodoloji.html   # Metodoloji açıklaması
├── ilçe.geojson           # İlçe sınırları
├── mahalle.json           # Mahalle sınırları
├── mahalle_nufus.xlsx     # Nüfus verileri
└── veri/
    └── veri.xlsx          # Sosyal veri
```

## 🎯 Özellikler

- 📍 İlçe ve mahalle bazında sosyal sorun haritası
- 🎨 Nüfus normalizasyonu (4. kök yöntemi)
- 🔍 Üst ve alt grup filtreleme
- 📊 Dezavantajlı grup analizi
- 📱 Responsive tasarım

## 📐 Metodoloji

Nüfus normalizasyonu için **4. kök (n^0.25)** yöntemi kullanılmaktadır:

```
Değer = Toplam / ⁴√Nüfus × 10
```

Bu yöntem nüfus etkisini %25 seviyesinde tutar, küçük nüfuslu bölgelerin abartılı görünmesini engeller.

Detaylı açıklama: [Metodoloji Sayfası](nufus_metodoloji.html)

## 📝 Lisans

MIT License

---

*İstanbul Sosyal Harita Projesi - 2026*
