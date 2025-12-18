# app.py
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import pandas as pd
import csv
import os
from datetime import datetime

# Import custom modules
import sys
sys.path.append(os.path.dirname(__file__))
from src.gradcam import generate_gradcam_visualization
from src.recommendations import get_recommendation, generate_report

# ========== CONFIG ==========
MODEL_PATH = 'models/waste_mobilenet.h5'
IMAGE_SIZE = (224, 224)
CLASS_NAMES = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
RECORDS_PATH = 'outputs/records.csv'
# ============================

st.set_page_config(
    page_title="Waste Vision - Deteksi Tumpukan Sampah",
    page_icon="🗑️",
    layout="wide"
)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

# Load model
try:
    model = load_model()
    model_loaded = True
except:
    model_loaded = False

# ========== HEADER ==========
st.title('🗑️ Waste Vision')
st.markdown('**Sistem Deteksi Tumpukan Sampah Berbasis CNN dengan Rekomendasi Penanganan**')
st.markdown('---')

# ========== SIDEBAR ==========
st.sidebar.header('📍 Input Lokasi')
location = st.sidebar.text_input('Nama Lokasi/Zona', placeholder='Contoh: Jl. Sudirman Blok A')
district = st.sidebar.selectbox('Kecamatan', ['Pilih Kecamatan', 'Kecamatan A', 'Kecamatan B', 'Kecamatan C', 'Lainnya'])
notes = st.sidebar.text_area('Catatan Tambahan', placeholder='Catatan opsional...')

st.sidebar.markdown('---')
st.sidebar.header('📊 Menu')
menu = st.sidebar.radio('Pilih Menu', ['🔍 Deteksi Baru', '📈 Riwayat & Heatmap'])

# ========== MAIN CONTENT ==========
if menu == '🔍 Deteksi Baru':
    if not model_loaded:
        st.error('⚠️ Model belum tersedia. Silakan training model terlebih dahulu.')
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('📤 Upload Gambar')
        uploaded = st.file_uploader('Pilih gambar tumpukan sampah', type=['jpg', 'png', 'jpeg', 'webp'])
        
        if uploaded:
            img = Image.open(uploaded).convert('RGB')
            st.image(img, caption='Gambar yang diupload', use_container_width=True)
    
    with col2:
        if uploaded:
            st.subheader('🎯 Hasil Deteksi')
            
            with st.spinner('Menganalisis gambar...'):
                # Generate Grad-CAM visualization
                result = generate_gradcam_visualization(model, img, IMAGE_SIZE)
                
                pred_idx = result['pred_index']
                label = CLASS_NAMES[pred_idx]
                confidence = result['confidence']
                
                # Get recommendation
                rec = get_recommendation(label)
            
            # Display result
            st.markdown(f"### {rec['status']}")
            st.metric('Confidence', f"{confidence*100:.1f}%")
            
            # Confidence bars
            st.markdown('**Probabilitas per Kelas:**')
            for i, cls in enumerate(CLASS_NAMES):
                prob = result['all_predictions'][i]
                st.progress(float(prob), text=f"{cls}: {prob*100:.1f}%")
            
            # Heatmap visualization
            st.markdown('---')
            st.subheader('🔥 Grad-CAM Heatmap')
            st.markdown('*Area merah menunjukkan region yang paling berpengaruh dalam deteksi*')
            
            heatmap_col1, heatmap_col2 = st.columns(2)
            with heatmap_col1:
                st.image(result['original'], caption='Original', use_container_width=True)
            with heatmap_col2:
                st.image(result['overlay'], caption='Heatmap Overlay', use_container_width=True)
    
    # Recommendations section
    if uploaded:
        st.markdown('---')
        st.subheader('📋 Rekomendasi Penanganan')
        
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            st.markdown(f"**Prioritas:** {rec['priority']}")
            st.markdown(f"**Timeline:** {rec['timeline']}")
        
        with rec_col2:
            st.markdown(f"**Resources:** {rec['resources']}")
        
        with rec_col3:
            st.markdown(f"**Priority Score:** {rec['priority_score']}")
        
        st.markdown('**Aksi yang Direkomendasikan:**')
        for i, action in enumerate(rec['actions'], 1):
            st.markdown(f"{i}. {action}")
        
        # Save record
        st.markdown('---')
        if st.button('💾 Simpan Record', type='primary'):
            if not location:
                st.warning('⚠️ Mohon isi nama lokasi terlebih dahulu di sidebar.')
            else:
                os.makedirs('outputs', exist_ok=True)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Check if file exists to write header
                file_exists = os.path.exists(RECORDS_PATH)
                
                with open(RECORDS_PATH, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['timestamp', 'filename', 'location', 'district', 'detection', 'confidence', 'priority_score', 'notes'])
                    writer.writerow([timestamp, uploaded.name, location, district, label, f"{confidence:.4f}", rec['priority_score'], notes])
                
                st.success(f'✅ Record berhasil disimpan!')
                st.balloons()

elif menu == '📈 Riwayat & Heatmap':
    st.subheader('📈 Riwayat Deteksi & Priority Heatmap')
    
    if os.path.exists(RECORDS_PATH):
        df = pd.read_csv(RECORDS_PATH)
        
        # Summary stats
        st.markdown('### 📊 Statistik')
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric('Total Deteksi', len(df))
        with stat_col2:
            parah_count = len(df[df['detection'] == 'tumpukan_parah'])
            st.metric('Tumpukan Parah', parah_count)
        with stat_col3:
            ringan_count = len(df[df['detection'] == 'tumpukan_ringan'])
            st.metric('Tumpukan Ringan', ringan_count)
        with stat_col4:
            bersih_count = len(df[df['detection'] == 'bersih'])
            st.metric('Bersih', bersih_count)
        
        # Priority heatmap by location
        st.markdown('### 🗺️ Priority Heatmap per Lokasi')
        st.markdown('*Semakin tinggi score, semakin urgent penanganan*')
        
        if 'location' in df.columns and len(df) > 0:
            location_summary = df.groupby('location').agg({
                'priority_score': ['sum', 'mean', 'count']
            }).reset_index()
            location_summary.columns = ['Lokasi', 'Total Score', 'Rata-rata Score', 'Jumlah Deteksi']
            location_summary = location_summary.sort_values('Total Score', ascending=False)
            
            # Bar chart
            st.bar_chart(location_summary.set_index('Lokasi')['Total Score'])
            
            # Table
            st.dataframe(location_summary, use_container_width=True)
        
        # Detection distribution
        st.markdown('### 📊 Distribusi Deteksi')
        detection_counts = df['detection'].value_counts()
        st.bar_chart(detection_counts)
        
        # Full records table
        st.markdown('### 📋 Riwayat Lengkap')
        st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)
        
        # Download button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='📥 Download Data CSV',
            data=csv_data,
            file_name='waste_detection_records.csv',
            mime='text/csv'
        )
    else:
        st.info('📭 Belum ada data deteksi. Silakan lakukan deteksi terlebih dahulu.')

# Footer
st.markdown('---')
st.markdown('*Waste Vision - Sistem Deteksi Tumpukan Sampah Berbasis CNN*')
