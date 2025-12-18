# src/recommendations.py
"""
Sistem rekomendasi berdasarkan hasil deteksi tumpukan sampah
"""

RECOMMENDATIONS = {
    'bersih': {
        'status': '✅ Bersih',
        'priority': 'Rendah',
        'priority_score': 0.1,
        'color': '#28a745',
        'actions': [
            'Pertahankan kebersihan area',
            'Lakukan monitoring rutin mingguan',
            'Pasang tanda "Jaga Kebersihan"'
        ],
        'timeline': 'Monitoring rutin setiap 7 hari',
        'resources': 'Minimal - 1 petugas monitoring'
    },
    'tumpukan_ringan': {
        'status': '⚠️ Tumpukan Ringan',
        'priority': 'Sedang',
        'priority_score': 0.6,
        'color': '#ffc107',
        'actions': [
            'Segera lakukan pembersihan dalam 1-2 hari',
            'Tambah tempat sampah di area sekitar',
            'Tingkatkan frekuensi pengangkutan sampah',
            'Sosialisasi ke warga sekitar tentang pembuangan sampah'
        ],
        'timeline': 'Pembersihan dalam 24-48 jam',
        'resources': 'Sedang - 2-3 petugas, 1 kendaraan pengangkut'
    },
    'tumpukan_parah': {
        'status': '🚨 Tumpukan Parah',
        'priority': 'Tinggi',
        'priority_score': 1.0,
        'color': '#dc3545',
        'actions': [
            'SEGERA lakukan pembersihan darurat',
            'Kerahkan tim pembersihan lengkap',
            'Koordinasi dengan Dinas Kebersihan',
            'Lakukan penyemprotan disinfektan setelah pembersihan',
            'Pasang CCTV untuk monitoring',
            'Identifikasi sumber pembuangan ilegal',
            'Buat laporan ke pihak berwenang'
        ],
        'timeline': 'Pembersihan SEGERA dalam 24 jam',
        'resources': 'Tinggi - 5+ petugas, 2+ kendaraan, alat berat jika diperlukan'
    }
}

def get_recommendation(class_name):
    """
    Dapatkan rekomendasi berdasarkan kelas deteksi
    
    Args:
        class_name: 'bersih', 'tumpukan_ringan', atau 'tumpukan_parah'
    
    Returns:
        dict berisi rekomendasi lengkap
    """
    return RECOMMENDATIONS.get(class_name, RECOMMENDATIONS['bersih'])

def generate_report(class_name, location, confidence, timestamp=None):
    """
    Generate laporan lengkap untuk satu deteksi
    
    Args:
        class_name: Hasil klasifikasi
        location: Nama lokasi/zona
        confidence: Confidence score
        timestamp: Waktu deteksi (optional)
    
    Returns:
        dict berisi laporan lengkap
    """
    from datetime import datetime
    
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    rec = get_recommendation(class_name)
    
    return {
        'timestamp': timestamp,
        'location': location,
        'detection_result': class_name,
        'confidence': confidence,
        'status': rec['status'],
        'priority': rec['priority'],
        'priority_score': rec['priority_score'],
        'recommended_actions': rec['actions'],
        'timeline': rec['timeline'],
        'resources_needed': rec['resources']
    }

def get_priority_summary(records_df):
    """
    Generate summary prioritas dari dataframe records
    
    Args:
        records_df: DataFrame dengan kolom location, detection, priority_score
    
    Returns:
        DataFrame summary per lokasi
    """
    import pandas as pd
    
    summary = records_df.groupby('location').agg({
        'priority_score': ['sum', 'mean', 'count'],
        'detection': lambda x: x.value_counts().index[0]  # most common
    }).reset_index()
    
    summary.columns = ['location', 'total_score', 'avg_score', 'detection_count', 'most_common']
    summary = summary.sort_values('total_score', ascending=False)
    
    return summary
