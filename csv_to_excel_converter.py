# -*- coding: utf-8 -*-
"""
Görüşme ve Gözlem Formu CSV → Normalize Excel Dönüştürücü
=========================================================
Bu script, Formidable Forms'dan export edilen wide-format CSV dosyasını
iki normalize edilmiş Excel sheet'ine dönüştürür.

Çıktılar:
1. Sosyal_Sorunlar: Sicil No, Aktör ID, Üst Grup, Alt Grup, Değer
2. Mahalle_Haritalama: Sicil No, Aktör ID, İlçe, Üst Grup, Alt Grup, Mahalle

Kullanım:
    python csv_to_excel_converter.py [input.csv] [output.xlsx]
    
Varsayılan:
    Input:  250924112528_1-görüşme-ve-gözlem-formu_formidable_entries.csv
    Output: gorusme_normalize.xlsx
"""

import pandas as pd
import re
import sys
from pathlib import Path


# =============================================================================
# YAPILANDIRMA
# =============================================================================

# Sabit sütunlar (her tabloya eklenecek)
BASE_COLUMNS = ['Personel Sicil No', 'Personel Ad Soyad', 'Aktör ID', 'Aktör Adı', 'Çalışma Alanı', 'Timestamp']

# Puan içeren sütun pattern'leri (Üst Grup - Alt Grup formatında)
SCORE_QUESTION_PATTERNS = [
    r"^Eğitim alanında en çok gözlemlenen sosyal sorunlar nelerdir\? - (.+)$",
    r"^Çalışma hayatında en çok gözlemlenen sosyal sorunlar nelerdir\? - (.+)$",
    r"^Ev hanımları düzensiz olarak en çok hangi işlerden ek gelir elde etmektedir\? - (.+)$",
    r"^Ayrımcılık alanında en çok gözlemlenen sosyal sorunlar nelerdir\? - (.+)$",
    r"^Şiddet alanında en çok gözlemlenen sosyal sorunlar nelerdir\? - (.+)$",
    r"^Diğer sosyal sorunlar en çok hangi alanda gözlemlenmektedir\? - (.+)$",
    r"^Bölgenizde yaşanan sosyal sorunlar nelerdir ve hangi yoğunlukta gözlemlenmektedir\? - (.+)$",
    r"^Bu dezavantajlı gruplarda yoğun olarak hangi sosyal sorunlar gözlemlenmektedir\? - (.+)$",
]

# Mahalle sütunları için pattern
# Format: "İlçe Seçiniz" ardından "Mahalle Seçiniz" veya "Mahalle" ardından "Seçim Yapınız" veya "Seçiniz"
ILCE_PATTERNS = [r"^İlçe Seçiniz$"]
MAHALLE_PATTERNS = [r"^Mahalle Seçiniz$", r"^Mahalle$"]
SECIM_PATTERNS = [r"^Seçim Yapınız$", r"^Seçiniz$"]


# =============================================================================
# YARDIMCI FONKSİYONLAR
# =============================================================================

def is_score_value(val):
    """Değerin geçerli bir puan olup olmadığını kontrol et (0-5)"""
    if pd.isna(val):
        return False
    try:
        score = int(float(str(val).strip()))
        return 0 <= score <= 5
    except (ValueError, TypeError):
        return False


def parse_score_column(col_name):
    """Sütun adından Üst Grup ve Alt Grup çıkar"""
    for pattern in SCORE_QUESTION_PATTERNS:
        match = re.match(pattern, col_name)
        if match:
            # Üst grubu pattern'den çıkar
            ust_grup = col_name.split(' - ')[0]
            alt_grup = match.group(1)
            return ust_grup, alt_grup
    return None, None


def split_mahalleler(mahalle_str):
    """Virgülle ayrılmış mahalleleri listeye çevir"""
    if pd.isna(mahalle_str) or str(mahalle_str).strip() == '':
        return []
    return [m.strip() for m in str(mahalle_str).split(',') if m.strip()]


def find_location_groups(columns):
    """
    Sütun listesinden İlçe-Mahalle-Seçim üçlülerini bul.
    Dinamik olarak sütun pozisyonlarına göre grupla.
    """
    groups = []
    i = 0
    
    while i < len(columns):
        col = columns[i]
        
        # İlçe sütunu mu?
        if any(re.match(p, col) for p in ILCE_PATTERNS):
            ilce_col = col
            ilce_idx = i
            
            # Sonraki sütunlar Mahalle ve Seçim mi?
            if i + 2 < len(columns):
                next_col = columns[i + 1]
                secim_col = columns[i + 2]
                
                is_mahalle = any(re.match(p, next_col) for p in MAHALLE_PATTERNS)
                is_secim = any(re.match(p, secim_col) for p in SECIM_PATTERNS)
                
                if is_mahalle and is_secim:
                    groups.append({
                        'ilce_idx': ilce_idx,
                        'mahalle_idx': i + 1,
                        'secim_idx': i + 2,
                        'ilce_col': col,
                        'mahalle_col': next_col,
                        'secim_col': secim_col
                    })
                    i += 3
                    continue
        i += 1
    
    return groups


def detect_ust_grup_for_location(columns, group_idx, location_groups):
    """
    Bir lokasyon grubu için hangi Üst Grup'a ait olduğunu belirle.
    Önceki puan sütunlarına bakarak bağlamı anla.
    """
    if group_idx >= len(location_groups):
        return "Bilinmeyen Grup"
    
    loc_group = location_groups[group_idx]
    ilce_col_idx = loc_group['ilce_idx']
    
    # Bu İlçe sütunundan önceki en yakın puan sütununu bul
    last_ust_grup = "Genel"
    
    for i in range(ilce_col_idx - 1, -1, -1):
        col = columns[i]
        ust_grup, _ = parse_score_column(col)
        if ust_grup:
            last_ust_grup = ust_grup
            break
    
    return last_ust_grup


# =============================================================================
# ANA DÖNÜŞÜM FONKSİYONLARI
# =============================================================================

def create_sosyal_sorunlar_table(df):
    """
    Sosyal Sorunlar Puanlama Tablosu oluştur.
    Her puan sütunu için ayrı satır.
    """
    rows = []
    columns = df.columns.tolist()
    
    # Puan sütunlarını bul
    score_columns = []
    for col in columns:
        ust_grup, alt_grup = parse_score_column(col)
        if ust_grup and alt_grup:
            score_columns.append((col, ust_grup, alt_grup))
    
    print(f"  → {len(score_columns)} puan sütunu bulundu")
    
    # Her satır ve her puan sütunu için kayıt oluştur
    for _, row in df.iterrows():
        base_data = {
            'Sicil No': row.get('Personel Sicil No', ''),
            'Personel Ad Soyad': row.get('Personel Ad Soyad', ''),
            'Aktör ID': row.get('Aktör ID', ''),
            'Aktör Adı': row.get('Aktör Adı', ''),
            'Çalışma Alanı': row.get('Çalışma Alanı', ''),
            'Timestamp': row.get('Timestamp', '')
        }
        
        for col, ust_grup, alt_grup in score_columns:
            val = row.get(col, '')
            
            # Sadece geçerli puan değerlerini al (0-5)
            if is_score_value(val):
                score = int(float(str(val).strip()))
                new_row = base_data.copy()
                new_row['Üst Grup'] = ust_grup
                new_row['Alt Grup'] = alt_grup
                new_row['Değer'] = score
                rows.append(new_row)
    
    result_df = pd.DataFrame(rows)
    
    # Sütun sırasını ayarla
    column_order = ['Sicil No', 'Personel Ad Soyad', 'Aktör ID', 'Aktör Adı', 
                    'Çalışma Alanı', 'Üst Grup', 'Alt Grup', 'Değer', 'Timestamp']
    result_df = result_df[[c for c in column_order if c in result_df.columns]]
    
    return result_df


def create_mahalle_table(df):
    """
    Mahalle Haritalama Tablosu oluştur.
    Her mahalle ayrı satırda.
    """
    rows = []
    columns = df.columns.tolist()
    
    # Lokasyon gruplarını bul
    location_groups = find_location_groups(columns)
    print(f"  → {len(location_groups)} lokasyon grubu (İlçe-Mahalle-Seçim) bulundu")
    
    # Her satır için
    for _, row in df.iterrows():
        base_data = {
            'Sicil No': row.get('Personel Sicil No', ''),
            'Personel Ad Soyad': row.get('Personel Ad Soyad', ''),
            'Aktör ID': row.get('Aktör ID', ''),
            'Aktör Adı': row.get('Aktör Adı', ''),
            'Çalışma Alanı': row.get('Çalışma Alanı', ''),
            'Timestamp': row.get('Timestamp', '')
        }
        
        for group_idx, loc_group in enumerate(location_groups):
            ilce = row.iloc[loc_group['ilce_idx']] if loc_group['ilce_idx'] < len(row) else ''
            mahalle_str = row.iloc[loc_group['mahalle_idx']] if loc_group['mahalle_idx'] < len(row) else ''
            secim = row.iloc[loc_group['secim_idx']] if loc_group['secim_idx'] < len(row) else ''
            
            # Boş ilçe veya mahalle varsa atla
            if pd.isna(ilce) or str(ilce).strip() == '':
                continue
            if pd.isna(mahalle_str) or str(mahalle_str).strip() == '':
                continue
            
            # Üst grubu belirle
            ust_grup = detect_ust_grup_for_location(columns, group_idx, location_groups)
            
            # Seçim (Alt Grup)
            alt_grup = str(secim).strip() if not pd.isna(secim) else ''
            
            # Mahalleleri böl
            mahalleler = split_mahalleler(mahalle_str)
            
            for mahalle in mahalleler:
                new_row = base_data.copy()
                new_row['İlçe'] = str(ilce).strip()
                new_row['Üst Grup'] = ust_grup
                new_row['Alt Grup'] = alt_grup
                new_row['Mahalle'] = mahalle
                rows.append(new_row)
    
    result_df = pd.DataFrame(rows)
    
    # Sütun sırasını ayarla
    column_order = ['Sicil No', 'Personel Ad Soyad', 'Aktör ID', 'Aktör Adı',
                    'Çalışma Alanı', 'İlçe', 'Üst Grup', 'Alt Grup', 'Mahalle', 'Timestamp']
    result_df = result_df[[c for c in column_order if c in result_df.columns]]
    
    return result_df


# =============================================================================
# ANA PROGRAM
# =============================================================================

def main():
    # Varsayılan dosya yolları
    script_dir = Path(__file__).parent
    default_input = script_dir / "250924112528_1-görüşme-ve-gözlem-formu_formidable_entries.csv"
    default_output = script_dir / "gorusme_normalize.xlsx"
    
    # Komut satırı argümanları
    input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else default_input
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output
    
    print("=" * 60)
    print("GÖRÜŞME VE GÖZLEM FORMU - CSV → EXCEL DÖNÜŞTÜRÜCÜ")
    print("=" * 60)
    print(f"\nGiriş dosyası: {input_file}")
    print(f"Çıkış dosyası: {output_file}")
    
    # CSV'yi oku
    print("\n[1/4] CSV dosyası okunuyor...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    print(f"  → {len(df)} satır, {len(df.columns)} sütun okundu")
    
    # Sosyal Sorunlar tablosu oluştur
    print("\n[2/4] Sosyal Sorunlar tablosu oluşturuluyor...")
    sosyal_df = create_sosyal_sorunlar_table(df)
    print(f"  → {len(sosyal_df)} kayıt oluşturuldu")
    
    # Mahalle tablosu oluştur
    print("\n[3/4] Mahalle Haritalama tablosu oluşturuluyor...")
    mahalle_df = create_mahalle_table(df)
    print(f"  → {len(mahalle_df)} kayıt oluşturuldu")
    
    # Excel'e yaz
    print("\n[4/4] Excel dosyası yazılıyor...")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        sosyal_df.to_excel(writer, sheet_name='Sosyal_Sorunlar', index=False)
        mahalle_df.to_excel(writer, sheet_name='Mahalle_Haritalama', index=False)
    
    print(f"\n✅ Dönüşüm tamamlandı!")
    print(f"   Çıktı: {output_file}")
    print(f"   - Sosyal_Sorunlar: {len(sosyal_df)} satır")
    print(f"   - Mahalle_Haritalama: {len(mahalle_df)} satır")
    print("=" * 60)


if __name__ == "__main__":
    main()
