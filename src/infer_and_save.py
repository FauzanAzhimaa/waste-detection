# src/infer_and_save.py
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import csv
from datetime import datetime
from utils import now_iso

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'waste_mobilenet.h5')
IMG_DIR = os.path.join(BASE_DIR, '..', 'data', 'test')
OUT_CSV = os.path.join(BASE_DIR, '..', 'outputs', 'records.csv')
IMAGE_SIZE = (224,224)
CLASS_NAMES = ['bersih','tumpukan_ringan','tumpukan_parah']  # pastikan urutan sesuai folder

def preprocess_img(path):
    img = image.load_img(path, target_size=IMAGE_SIZE)
    arr = image.img_to_array(img)/255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

def main():
    model = tf.keras.models.load_model(MODEL_PATH)
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','image','zone_id','label','confidence','priority_score'])
        # if IMG_DIR has subfolders (classes), iterate
        for root, dirs, files in os.walk(IMG_DIR):
            for fname in files:
                if not fname.lower().endswith(('.jpg','.png','.jpeg')): continue
                p = os.path.join(root, fname)
                arr = preprocess_img(p)
                probs = model.predict(arr)[0]
                idx = int(np.argmax(probs))
                label = CLASS_NAMES[idx]
                conf = float(probs[idx])
                # zone_id: if you have metadata, map here. For now: use folder name or 'unknown'
                zone = os.path.basename(root) if root!=IMG_DIR else 'unknown'
                # map to priority score
                if label == 'tumpukan_parah':
                    priority = 1.0
                elif label == 'tumpukan_ringan':
                    priority = 0.6
                else:
                    priority = 0.1
                writer.writerow([datetime.utcnow().isoformat(), fname, zone, label, conf, priority])
    print('Saved predictions to', OUT_CSV)

if __name__ == '__main__':
    main()
