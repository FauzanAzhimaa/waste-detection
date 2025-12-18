"""
Model Performance Analysis - Kampus 1 UNJANI Yogyakarta
Analisis detail performa model deteksi sampah
"""
import numpy as np
import tensorflow as tf
from pathlib import Path
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from PIL import Image


class ModelAnalyzer:
    """Analisis performa model"""
    
    def __init__(self, model_path, data_dir):
        self.model_path = Path(model_path)
        self.data_dir = Path(data_dir)
        self.class_names = ['Bersih', 'Tumpukan Parah', 'Tumpukan Ringan']
        self.image_size = (224, 224)
        
        # Load model
        print("📦 Loading model...")
        self.model = tf.keras.models.load_model(str(self.model_path))
        print("✅ Model loaded successfully\n")
    
    def analyze_dataset_distribution(self):
        """Analisis distribusi dataset"""
        print("=" * 70)
        print("📊 ANALISIS DISTRIBUSI DATASET")
        print("=" * 70)
        
        categories = ['bersih', 'tumpukan_parah', 'tumpukan_ringan']
        splits = ['train', 'val', 'test']
        
        distribution = {}
        
        for split in splits:
            split_path = self.data_dir / split
            if not split_path.exists():
                continue
            
            print(f"\n📁 {split.upper()} SET:")
            split_data = {}
            
            for category in categories:
                category_path = split_path / category
                if category_path.exists():
                    images = list(category_path.glob('*.jpg')) + \
                            list(category_path.glob('*.jpeg')) + \
                            list(category_path.glob('*.png')) + \
                            list(category_path.glob('*.webp'))
                    count = len(images)
                    split_data[category] = count
                    
                    # Display name mapping
                    display_name = {
                        'bersih': 'Bersih',
                        'tumpukan_parah': 'Tumpukan Parah',
                        'tumpukan_ringan': 'Tumpukan Ringan'
                    }[category]
                    
                    print(f"   {display_name:20s}: {count:3d} gambar")
                else:
                    split_data[category] = 0
            
            total = sum(split_data.values())
            print(f"   {'TOTAL':20s}: {total:3d} gambar")
            
            # Cek balance
            if total > 0:
                percentages = {k: (v/total)*100 for k, v in split_data.items()}
                print(f"\n   Distribusi:")
                for cat, pct in percentages.items():
                    display_name = {
                        'bersih': 'Bersih',
                        'tumpukan_parah': 'Tumpukan Parah',
                        'tumpukan_ringan': 'Tumpukan Ringan'
                    }[cat]
                    bar = '█' * int(pct / 2)
                    print(f"   {display_name:20s}: {pct:5.1f}% {bar}")
                
                # Warning jika tidak seimbang
                max_pct = max(percentages.values())
                min_pct = min(percentages.values())
                if max_pct - min_pct > 20:
                    print(f"\n   ⚠️ WARNING: Dataset tidak seimbang!")
                    print(f"   Selisih: {max_pct - min_pct:.1f}%")
                    print(f"   Rekomendasi: Tambah data untuk kategori dengan jumlah sedikit")
            
            distribution[split] = split_data
        
        return distribution
    
    def evaluate_on_test_set(self):
        """Evaluasi model pada test set"""
        print("\n" + "=" * 70)
        print("🎯 EVALUASI PADA TEST SET")
        print("=" * 70)
        
        test_dir = self.data_dir / 'test'
        if not test_dir.exists():
            print("❌ Test set tidak ditemukan!")
            return None
        
        # Load test data
        print("\n📂 Loading test data...")
        test_images = []
        test_labels = []
        test_filenames = []
        
        categories = ['bersih', 'tumpukan_parah', 'tumpukan_ringan']
        label_map = {'bersih': 0, 'tumpukan_parah': 1, 'tumpukan_ringan': 2}
        
        for category in categories:
            category_path = test_dir / category
            if not category_path.exists():
                continue
            
            images = list(category_path.glob('*.jpg')) + \
                    list(category_path.glob('*.jpeg')) + \
                    list(category_path.glob('*.png')) + \
                    list(category_path.glob('*.webp'))
            
            for img_path in images:
                try:
                    img = Image.open(img_path).convert('RGB')
                    img = img.resize(self.image_size)
                    img_array = np.array(img) / 255.0
                    
                    test_images.append(img_array)
                    test_labels.append(label_map[category])
                    test_filenames.append(img_path.name)
                except Exception as e:
                    print(f"⚠️ Error loading {img_path.name}: {e}")
        
        if len(test_images) == 0:
            print("❌ Tidak ada gambar test yang valid!")
            return None
        
        test_images = np.array(test_images)
        test_labels = np.array(test_labels)
        
        print(f"✅ Loaded {len(test_images)} test images\n")
        
        # Predict
        print("🔮 Making predictions...")
        predictions = self.model.predict(test_images, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        # Calculate metrics
        accuracy = np.mean(predicted_classes == test_labels)
        
        print(f"\n📊 OVERALL ACCURACY: {accuracy * 100:.2f}%\n")
        
        # Confusion Matrix
        cm = confusion_matrix(test_labels, predicted_classes)
        
        print("📈 CONFUSION MATRIX:")
        print("=" * 70)
        print(f"{'':20s} {'Predicted →':^40s}")
        print(f"{'Actual ↓':20s} {'Bersih':^13s} {'Tumpukan Parah':^13s} {'Tumpukan Ringan':^13s}")
        print("-" * 70)
        
        for i, class_name in enumerate(self.class_names):
            row = f"{class_name:20s}"
            for j in range(len(self.class_names)):
                row += f" {cm[i][j]:^13d}"
            print(row)
        
        print("=" * 70)
        
        # Per-class metrics
        print("\n📊 PER-CLASS METRICS:")
        print("=" * 70)
        
        for i, class_name in enumerate(self.class_names):
            class_mask = test_labels == i
            class_predictions = predicted_classes[class_mask]
            class_true = test_labels[class_mask]
            
            if len(class_true) > 0:
                class_accuracy = np.mean(class_predictions == class_true)
                
                # Precision & Recall
                tp = np.sum((predicted_classes == i) & (test_labels == i))
                fp = np.sum((predicted_classes == i) & (test_labels != i))
                fn = np.sum((predicted_classes != i) & (test_labels == i))
                
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                
                print(f"\n{class_name}:")
                print(f"   Accuracy:  {class_accuracy * 100:6.2f}%")
                print(f"   Precision: {precision * 100:6.2f}%")
                print(f"   Recall:    {recall * 100:6.2f}%")
                print(f"   F1-Score:  {f1 * 100:6.2f}%")
                print(f"   Samples:   {len(class_true)}")
        
        print("=" * 70)
        
        # Misclassified examples
        print("\n❌ MISCLASSIFIED EXAMPLES:")
        print("=" * 70)
        
        misclassified = predicted_classes != test_labels
        if np.sum(misclassified) > 0:
            print(f"\nTotal misclassified: {np.sum(misclassified)}/{len(test_labels)}\n")
            
            for i, (pred, true, filename) in enumerate(zip(predicted_classes[misclassified], 
                                                           test_labels[misclassified],
                                                           np.array(test_filenames)[misclassified])):
                if i >= 10:  # Show max 10 examples
                    print(f"... dan {np.sum(misclassified) - 10} lainnya")
                    break
                
                print(f"{i+1}. {filename}")
                print(f"   True: {self.class_names[true]:20s} → Predicted: {self.class_names[pred]}")
                print(f"   Confidence: {predictions[misclassified][i][pred] * 100:.1f}%\n")
        else:
            print("✅ Tidak ada misclassification! (Perfect score)")
        
        return {
            'accuracy': accuracy,
            'confusion_matrix': cm.tolist(),
            'total_samples': len(test_labels),
            'misclassified': int(np.sum(misclassified))
        }
    
    def analyze_confidence_distribution(self):
        """Analisis distribusi confidence predictions"""
        print("\n" + "=" * 70)
        print("📊 ANALISIS CONFIDENCE DISTRIBUTION")
        print("=" * 70)
        
        test_dir = self.data_dir / 'test'
        if not test_dir.exists():
            print("❌ Test set tidak ditemukan!")
            return
        
        # Load test data
        test_images = []
        test_labels = []
        
        categories = ['bersih', 'tumpukan_parah', 'tumpukan_ringan']
        label_map = {'bersih': 0, 'tumpukan_parah': 1, 'tumpukan_ringan': 2}
        
        for category in categories:
            category_path = test_dir / category
            if not category_path.exists():
                continue
            
            images = list(category_path.glob('*.jpg')) + \
                    list(category_path.glob('*.jpeg')) + \
                    list(category_path.glob('*.png')) + \
                    list(category_path.glob('*.webp'))
            
            for img_path in images:
                try:
                    img = Image.open(img_path).convert('RGB')
                    img = img.resize(self.image_size)
                    img_array = np.array(img) / 255.0
                    
                    test_images.append(img_array)
                    test_labels.append(label_map[category])
                except:
                    pass
        
        if len(test_images) == 0:
            return
        
        test_images = np.array(test_images)
        predictions = self.model.predict(test_images, verbose=0)
        max_confidences = np.max(predictions, axis=1)
        
        print(f"\n📈 Confidence Statistics:")
        print(f"   Mean:   {np.mean(max_confidences) * 100:.2f}%")
        print(f"   Median: {np.median(max_confidences) * 100:.2f}%")
        print(f"   Min:    {np.min(max_confidences) * 100:.2f}%")
        print(f"   Max:    {np.max(max_confidences) * 100:.2f}%")
        print(f"   Std:    {np.std(max_confidences) * 100:.2f}%")
        
        # Confidence ranges
        print(f"\n📊 Confidence Ranges:")
        ranges = [
            (0.9, 1.0, "Sangat Tinggi (90-100%)"),
            (0.8, 0.9, "Tinggi (80-90%)"),
            (0.7, 0.8, "Sedang (70-80%)"),
            (0.6, 0.7, "Rendah (60-70%)"),
            (0.0, 0.6, "Sangat Rendah (<60%)")
        ]
        
        for low, high, label in ranges:
            count = np.sum((max_confidences >= low) & (max_confidences < high))
            percentage = (count / len(max_confidences)) * 100
            bar = '█' * int(percentage / 2)
            print(f"   {label:25s}: {count:3d} ({percentage:5.1f}%) {bar}")
    
    def generate_recommendations(self):
        """Generate rekomendasi perbaikan"""
        print("\n" + "=" * 70)
        print("💡 REKOMENDASI PERBAIKAN MODEL")
        print("=" * 70)
        
        # Analyze current state
        distribution = self.analyze_dataset_distribution()
        
        print("\n🎯 REKOMENDASI:")
        print("-" * 70)
        
        # Check dataset size
        total_train = sum(distribution.get('train', {}).values())
        if total_train < 500:
            print("\n1. ⚠️ DATASET TERLALU KECIL")
            print(f"   Current: {total_train} gambar training")
            print(f"   Target:  900-1500 gambar training (300-500 per kategori)")
            print(f"   Action:  Kumpulkan {900 - total_train} gambar lagi")
            print(f"   Priority: 🔴 CRITICAL")
        
        # Check balance
        if 'train' in distribution:
            train_data = distribution['train']
            if train_data:
                max_count = max(train_data.values())
                min_count = min(train_data.values())
                imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
                
                if imbalance_ratio > 1.5:
                    print("\n2. ⚠️ DATASET TIDAK SEIMBANG")
                    print(f"   Ratio: {imbalance_ratio:.2f}x")
                    for cat, count in train_data.items():
                        display_name = {
                            'bersih': 'Bersih',
                            'tumpukan_parah': 'Tumpukan Parah',
                            'tumpukan_ringan': 'Tumpukan Ringan'
                        }[cat]
                        print(f"   {display_name}: {count} gambar")
                    print(f"   Action:  Tambah data untuk kategori dengan jumlah sedikit")
                    print(f"   Priority: 🟡 HIGH")
        
        print("\n3. 📸 TIPS PENGUMPULAN DATA:")
        print("   ✅ Foto dari berbagai sudut (depan, samping, atas)")
        print("   ✅ Berbagai waktu (pagi, siang, sore)")
        print("   ✅ Berbagai kondisi pencahayaan")
        print("   ✅ Berbagai lokasi di kampus")
        print("   ✅ Berbagai jenis dan jumlah sampah")
        
        print("\n4. 🔄 TRAINING RECOMMENDATIONS:")
        print("   • Gunakan data augmentation (sudah ada)")
        print("   • Training dengan lebih banyak epochs (20-30)")
        print("   • Gunakan learning rate scheduling")
        print("   • Monitor overfitting dengan validation loss")
        
        print("\n5. 📊 MONITORING:")
        print("   • Jalankan script ini setelah setiap training")
        print("   • Cek confusion matrix untuk pattern kesalahan")
        print("   • Analisis misclassified examples")
        print("   • Track improvement dari waktu ke waktu")
        
        print("=" * 70)
    
    def save_report(self, output_path='model_analysis_report.json'):
        """Save analysis report to JSON"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'model_path': str(self.model_path),
            'data_dir': str(self.data_dir),
            'distribution': {},
            'evaluation': None
        }
        
        # Get distribution
        distribution = self.analyze_dataset_distribution()
        report['distribution'] = distribution
        
        # Get evaluation
        eval_results = self.evaluate_on_test_set()
        if eval_results:
            report['evaluation'] = eval_results
        
        # Save
        output_file = Path(output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Report saved to: {output_file}")
        return report


def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    model_path = base_dir / 'models' / 'waste_mobilenet.h5'
    data_dir = base_dir / 'data'
    
    if not model_path.exists():
        print(f"❌ Model tidak ditemukan di: {model_path}")
        return
    
    if not data_dir.exists():
        print(f"❌ Data directory tidak ditemukan di: {data_dir}")
        return
    
    print("\n" + "=" * 70)
    print("🔍 MODEL PERFORMANCE ANALYSIS")
    print("   Kampus 1 UNJANI Yogyakarta")
    print("=" * 70)
    
    analyzer = ModelAnalyzer(model_path, data_dir)
    
    # Run all analyses
    analyzer.analyze_dataset_distribution()
    analyzer.evaluate_on_test_set()
    analyzer.analyze_confidence_distribution()
    analyzer.generate_recommendations()
    
    # Save report
    analyzer.save_report()
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
