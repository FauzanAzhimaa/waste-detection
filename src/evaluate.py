# src/evaluate.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'waste_mobilenet.h5')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
IMAGE_SIZE = (224,224)
BATCH_SIZE = 16

def main():
    model = tf.keras.models.load_model(MODEL_PATH)
    val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
        os.path.join(DATA_DIR,'test'),
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    preds = model.predict(val_gen, verbose=1)
    y_pred = np.argmax(preds, axis=1)
    y_true = val_gen.classes
    labels = list(val_gen.class_indices.keys())

    print(classification_report(y_true, y_pred, target_names=labels))
    cm = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)
    plt.figure(figsize=(6,4))
    sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted'); plt.ylabel('True')
    plt.title('Confusion Matrix')
    out_png = os.path.join(BASE_DIR, '..', 'outputs', 'confusion_matrix.png')
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, dpi=200)
    print('Saved confusion matrix to', out_png)

if __name__ == '__main__':
    main()
