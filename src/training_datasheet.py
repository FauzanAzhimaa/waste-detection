# src/training_datasheet.py
"""
Script untuk generate datasheet hasil training model
"""
import os
import json
import pandas as pd
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'waste_mobilenet.h5')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'outputs')
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16

def generate_training_datasheet(history=None, model=None):
    """
    Generate datasheet lengkap hasil training
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    datasheet = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'model_path': MODEL_PATH,
            'image_size': IMAGE_SIZE,
            'batch_size': BATCH_SIZE
        },
        'dataset_info': {},
        'training_history': {},
        'evaluation_metrics': {}
    }
    
    # Dataset info
    for split in ['train', 'val', 'test']:
        split_path = os.path.join(DATA_DIR, split)
        if os.path.exists(split_path):
            class_counts = {}
            for cls in os.listdir(split_path):
                cls_path = os.path.join(split_path, cls)
                if os.path.isdir(cls_path):
                    class_counts[cls] = len([f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            datasheet['dataset_info'][split] = {
                'total': sum(class_counts.values()),
                'per_class': class_counts
            }
    
    # Training history
    if history:
        datasheet['training_history'] = {
            'epochs': len(history.get('accuracy', [])),
            'final_accuracy': history.get('accuracy', [0])[-1],
            'final_val_accuracy': history.get('val_accuracy', [0])[-1],
            'final_loss': history.get('loss', [0])[-1],
            'final_val_loss': history.get('val_loss', [0])[-1],
            'accuracy_history': history.get('accuracy', []),
            'val_accuracy_history': history.get('val_accuracy', []),
            'loss_history': history.get('loss', []),
            'val_loss_history': history.get('val_loss', [])
        }
    
    # Evaluation on test set
    if model is None and os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
    
    if model:
        test_path = os.path.join(DATA_DIR, 'test')
        if os.path.exists(test_path):
            test_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
                test_path,
                target_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
                class_mode='categorical',
                shuffle=False
            )
            
            preds = model.predict(test_gen, verbose=0)
            y_pred = np.argmax(preds, axis=1)
            y_true = test_gen.classes
            labels = list(test_gen.class_indices.keys())
            
            # Classification report
            report = classification_report(y_true, y_pred, target_names=labels, output_dict=True)
            cm = confusion_matrix(y_true, y_pred).tolist()
            
            datasheet['evaluation_metrics'] = {
                'test_accuracy': report['accuracy'],
                'classification_report': report,
                'confusion_matrix': cm,
                'class_labels': labels
            }
    
    # Save as JSON
    json_path = os.path.join(OUTPUT_DIR, f'training_datasheet_{timestamp}.json')
    with open(json_path, 'w') as f:
        json.dump(datasheet, f, indent=2, default=str)
    
    # Save as CSV summary
    csv_path = os.path.join(OUTPUT_DIR, f'training_summary_{timestamp}.csv')
    summary_data = []
    
    for split, info in datasheet['dataset_info'].items():
        for cls, count in info.get('per_class', {}).items():
            summary_data.append({
                'split': split,
                'class': cls,
                'count': count
            })
    
    if summary_data:
        pd.DataFrame(summary_data).to_csv(csv_path, index=False)
    
    print(f"Datasheet saved to: {json_path}")
    print(f"Summary saved to: {csv_path}")
    
    return datasheet

if __name__ == '__main__':
    datasheet = generate_training_datasheet()
    print("\n=== TRAINING DATASHEET ===")
    print(json.dumps(datasheet, indent=2, default=str))
