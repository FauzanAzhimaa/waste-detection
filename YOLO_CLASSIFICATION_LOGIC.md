# Logika Klasifikasi YOLO - Sistem Deteksi Sampah

## Update Terbaru: Improved Clustering & Classification Logic

### Masalah Sebelumnya
- Logika spatial clustering terlalu sederhana (hanya jarak rata-rata)
- Threshold terlalu kaku (normalized distance < 3.0)
- Tidak mempertimbangkan kepadatan dan jumlah objek dengan baik

### Solusi Baru

#### 1. Improved Spatial Clustering Analysis
Fungsi `_analyze_pile_clustering()` sekarang menggunakan 3 metrik:

**a) Density (Kepadatan)**
```
density = total_object_area / spread_area
```
- Mengukur seberapa padat objek dalam area yang mereka tempati
- Density > 0.3 = PILED (objek sangat padat)
- Density > 0.15 dengan >10 objek = PILED

**b) Proximity (Kedekatan)**
```
normalized_distance = avg_nearest_neighbor_distance / avg_bbox_size
```
- Mengukur jarak rata-rata ke tetangga terdekat
- Normalized distance < 2.5 = PILED (objek sangat dekat)

**c) Object Count (Jumlah)**
- >10 objek dengan density >0.15 = PILED

#### 2. Improved Classification Logic

**Kategori "Bersih"**
- 0 objek terdeteksi
- Confidence: 95%

**Kategori "Tumpukan Ringan"**
- 1-2 objek berserakan (dengan warning: mungkin ada objek kecil tidak terdeteksi)
- 3-8 objek berserakan (tidak menumpuk)
- Confidence: 95%

**Kategori "Tumpukan Parah"**
- Objek menumpuk (is_piled = True) - apapun jumlahnya
- >8 objek meskipun berserakan (terlalu banyak sampah)
- Confidence: 95%

### Kriteria "Piled" (Menumpuk)
Objek dianggap menumpuk jika memenuhi SALAH SATU:
1. **Density > 0.3** - Objek sangat padat dalam area kecil
2. **Normalized distance < 2.5** - Objek sangat dekat satu sama lain
3. **>10 objek dengan density > 0.15** - Banyak objek dengan kepadatan sedang

### Contoh Skenario

| Jumlah Objek | Piled? | Density | Hasil Klasifikasi |
|--------------|--------|---------|-------------------|
| 0 | - | - | **Bersih** |
| 1-2 | No | Low | **Tumpukan Ringan** (+ warning) |
| 3-8 | No | Low | **Tumpukan Ringan** |
| 3-8 | Yes | High | **Tumpukan Parah** |
| 9+ | No | Low | **Tumpukan Parah** (terlalu banyak) |
| 9+ | Yes | High | **Tumpukan Parah** |

### Output Console
Setiap analisis akan menampilkan:
```
📏 Clustering: count=5, density=0.245, norm_dist=3.12 → SCATTERED
⚠️ YOLO: 5 objek sampah berserakan → Tumpukan Ringan
```

atau

```
📏 Clustering: count=12, density=0.412, norm_dist=1.85 → PILED
🚨 YOLO: 12 objek MENUMPUK (kepadatan tinggi) → Tumpukan Parah
```

### Keunggulan Logika Baru
1. ✅ Lebih akurat membedakan tumpukan vs berserakan
2. ✅ Mempertimbangkan kepadatan area
3. ✅ Menangani edge case (banyak objek berserakan = tetap parah)
4. ✅ Lebih robust terhadap berbagai ukuran dan distribusi objek
5. ✅ Output yang lebih informatif untuk debugging

### File yang Dimodifikasi
- `app.py` - Fungsi `_analyze_pile_clustering()` (line ~835)
- `app.py` - YOLO override logic (line ~725)

### Testing
Coba upload gambar dengan berbagai kondisi:
1. Area bersih (0 objek)
2. 1-2 sampah kecil berserakan
3. 3-8 sampah berserakan
4. Sampah menumpuk (apapun jumlahnya)
5. >8 sampah berserakan

Perhatikan output console untuk melihat metrik clustering.
