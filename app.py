"""
Flask Web Application for Waste Detection - Kampus 1 UNJANI Yogyakarta
Using Object-Oriented Programming principles with PostgreSQL + Cloudinary
"""
# Set environment variables before importing TensorFlow
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN

from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import tensorflow as tf
from datetime import datetime, timezone, timedelta
import json
import cv2
import base64
from io import BytesIO

# Import database and cloudinary helpers
try:
    from database import DatabaseManager
    from cloudinary_helper import CloudinaryManager
    USE_DATABASE = True
    print("✓ Database and Cloudinary modules loaded")
except ImportError as e:
    print(f"⚠️ Database/Cloudinary not available: {e}")
    print("⚠️ Falling back to JSON file storage")
    USE_DATABASE = False


class Config:
    """Application configuration for Kampus 1 UNJAYA"""
    BASE_DIR = Path(__file__).parent
    MODEL_PATH = BASE_DIR / 'models' / 'waste_mobilenet.h5'
    
    # Temporary folder for processing (will be deleted after upload to cloud)
    TEMP_FOLDER = BASE_DIR / 'temp'
    
    # Fallback for JSON storage if database not available
    LOG_FILE = BASE_DIR / 'detection_logs.json'
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    IMAGE_SIZE = (224, 224)
    CLASS_NAMES = ['Bersih', 'Tumpukan Parah', 'Tumpukan Ringan']
    
    # Kampus 1 UNJANI Yogyakarta specific settings
    CAMPUS_NAME = "Kampus 1 Universitas Jenderal Achmad Yani Yogyakarta"
    CAMPUS_SHORT = "Kampus 1 UNJANI Yogyakarta"
    
    # Database and Cloud Storage
    USE_DATABASE = USE_DATABASE
    
    @classmethod
    def init_folders(cls):
        """Create necessary folders"""
        cls.TEMP_FOLDER.mkdir(exist_ok=True)
        print(f"📁 Temp folder: {cls.TEMP_FOLDER}")
        if not cls.USE_DATABASE:
            print(f"📝 Log file (fallback): {cls.LOG_FILE}")


class ImageMetadataExtractor:
    """Extract metadata from images including GPS"""
    
    @staticmethod
    def get_gps_data(image_path):
        """Extract GPS coordinates from image EXIF data"""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if not exif_data:
                return None
            
            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'GPSInfo':
                    for gps_tag in value:
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_info[gps_tag_name] = value[gps_tag]
            
            if not gps_info:
                return None
            
            # Convert GPS data to decimal degrees
            lat = ImageMetadataExtractor._convert_to_degrees(gps_info.get('GPSLatitude'))
            lon = ImageMetadataExtractor._convert_to_degrees(gps_info.get('GPSLongitude'))
            
            if lat and lon:
                lat_ref = gps_info.get('GPSLatitudeRef', 'N')
                lon_ref = gps_info.get('GPSLongitudeRef', 'E')
                
                if lat_ref == 'S':
                    lat = -lat
                if lon_ref == 'W':
                    lon = -lon
                
                return {'latitude': lat, 'longitude': lon}
            
        except Exception as e:
            print(f"GPS extraction error: {e}")
        
        return None
    
    @staticmethod
    def _convert_to_degrees(value):
        """Convert GPS coordinates to degrees"""
        if not value:
            return None
        d, m, s = value
        return float(d) + float(m) / 60.0 + float(s) / 3600.0


class WasteDetectionModel:
    """Model handler for waste detection"""
    
    def __init__(self, model_path, class_names, image_size=(224, 224)):
        self.model_path = model_path
        self.class_names = class_names
        self.image_size = image_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model with TensorFlow workaround"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        try:
            # Workaround for TensorFlow memory issue on Railway
            import gc
            gc.collect()
            
            # Disable GPU to prevent CUDA errors
            try:
                tf.config.set_visible_devices([], 'GPU')
            except:
                pass  # Ignore if GPU config fails
            
            # Load model - simple and clean
            print(f"📦 Loading model from {self.model_path}...")
            self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
            
            print(f"✓ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        img = Image.open(image_path).convert('RGB')
        img = img.resize(self.image_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path):
        """Make prediction on image"""
        img_array = self.preprocess_image(image_path)
        predictions = self.model.predict(img_array, verbose=0)
        
        class_idx = int(np.argmax(predictions[0]))  # Convert to Python int
        confidence = float(predictions[0][class_idx])
        class_name = self.class_names[class_idx]
        
        # Get all probabilities
        probabilities = {
            self.class_names[i]: float(predictions[0][i])
            for i in range(len(self.class_names))
        }
        
        return {
            'class': class_name,
            'confidence': confidence,
            'probabilities': probabilities,
            'class_idx': class_idx
        }
    
    def generate_gradcam(self, image_path, pred_index=None):
        """Generate Grad-CAM heatmap - memory efficient version"""
        try:
            print(f"🔥 Starting Grad-CAM generation...")
            
            # Load original image
            img_pil = Image.open(image_path).convert('RGB')
            original_size = img_pil.size  # Save original size
            print(f"✓ Original image size: {original_size}")
            
            # Limit max size to prevent memory issues on Railway
            max_dimension = 800
            if max(original_size) > max_dimension:
                ratio = max_dimension / max(original_size)
                new_size = tuple(int(dim * ratio) for dim in original_size)
                img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
                original_size = new_size
                print(f"✓ Resized to: {original_size} (memory optimization)")
            
            # Resize for model
            img_resized = img_pil.resize(self.image_size)
            img_array = np.array(img_resized, dtype=np.float32) / 255.0
            img_batch = np.expand_dims(img_array, 0)
            
            # Find last conv layer - simplified approach
            target_layer = None
            layer_name = None
            
            # Try to find the last conv layer in MobileNetV2
            for layer in reversed(self.model.layers):
                if hasattr(layer, 'layers'):
                    # It's a nested model (MobileNetV2)
                    for sublayer in reversed(layer.layers):
                        if 'conv' in sublayer.name.lower() and 'pw' in sublayer.name.lower():
                            target_layer = sublayer
                            layer_name = sublayer.name
                            break
                    if target_layer:
                        break
            
            if not target_layer:
                print("❌ No suitable conv layer found")
                return None
            
            print(f"✓ Using layer: {layer_name}")
            
            # Create grad model
            from tensorflow.keras.models import Model
            grad_model = Model(
                inputs=self.model.input,
                outputs=[target_layer.output, self.model.output]
            )
            
            # Compute gradients
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_batch)
                if pred_index is None:
                    pred_index = tf.argmax(predictions[0])
                class_channel = predictions[:, pred_index]
            
            grads = tape.gradient(class_channel, conv_outputs)
            
            if grads is None:
                print("❌ Gradients are None")
                return None
            
            # Compute heatmap
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0)
            
            max_val = tf.math.reduce_max(heatmap)
            if max_val > 0:
                heatmap = heatmap / max_val
            heatmap = heatmap.numpy()
            
            print(f"✓ Heatmap computed, shape: {heatmap.shape}")
            
            # Resize heatmap to original image size
            heatmap_resized = cv2.resize(heatmap, original_size)
            heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
            
            # Create overlay with original size image
            original_array = np.array(img_pil, dtype=np.float32)
            overlay = heatmap_colored * 0.6 + original_array * 0.4
            overlay = np.clip(overlay, 0, 255).astype(np.uint8)
            
            print("✓ Heatmap generated successfully")
            return overlay
            
        except MemoryError as e:
            print(f"❌ Memory error during Grad-CAM: {e}")
            return None
        except Exception as e:
            print(f"❌ Grad-CAM error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_recommendation(self, class_name, confidence):
        """Get recommendation based on prediction for Kampus 1 UNJAYA"""
        recommendations = {
            'Bersih': {
                'status': 'success',
                'message': 'Area Kampus 1 UNJANI Yogyakarta dalam kondisi bersih',
                'action': 'Pertahankan kebersihan area kampus',
                'priority': 'low',
                'pic': 'Tim Kebersihan Kampus'
            },
            'Tumpukan Ringan': {
                'status': 'warning',
                'message': 'Terdeteksi sampah ringan di area Kampus 1 UNJANI Yogyakarta',
                'action': 'Segera bersihkan sebelum menumpuk. Hubungi Tim Kebersihan Kampus',
                'priority': 'medium',
                'pic': 'Tim Kebersihan Kampus / Mahasiswa Piket'
            },
            'Tumpukan Parah': {
                'status': 'danger',
                'message': 'Tumpukan sampah parah terdeteksi di Kampus 1 UNJANI Yogyakarta!',
                'action': 'Perlu pembersihan segera dan menyeluruh. Laporkan ke Bagian Umum & Fasilitas',
                'priority': 'high',
                'pic': 'Bagian Umum & Fasilitas UNJANI Yogyakarta'
            }
        }
        
        rec = recommendations.get(class_name, recommendations['Bersih'])
        rec['confidence_level'] = 'Tinggi' if confidence > 0.8 else 'Sedang' if confidence > 0.6 else 'Rendah'
        rec['campus'] = Config.CAMPUS_SHORT
        return rec


class WasteDetectionApp:
    """Main Flask application class"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        Config.init_folders()
        
        # Initialize model
        self.model_handler = WasteDetectionModel(
            Config.MODEL_PATH,
            Config.CLASS_NAMES,
            Config.IMAGE_SIZE
        )
        
        # Initialize database and cloudinary if available
        self.db = None
        self.cloudinary = None
        
        if Config.USE_DATABASE:
            try:
                self.db = DatabaseManager()
                self.cloudinary = CloudinaryManager()
                print("✓ Database and Cloudinary initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize database/cloudinary: {e}")
                print("⚠️ Falling back to JSON storage")
                Config.USE_DATABASE = False
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register all application routes"""
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/predict', 'predict', self.predict, methods=['POST'])
        self.app.add_url_rule('/uploads/<filename>', 'uploaded_file', self.uploaded_file)
        self.app.add_url_rule('/history', 'history', self.history)
        self.app.add_url_rule('/api/logs', 'get_logs', self.get_logs)
        self.app.add_url_rule('/map', 'campus_map', self.campus_map)
        self.app.add_url_rule('/api/map-data', 'get_map_data', self.get_map_data)
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    def index(self):
        """Home page"""
        return render_template('index.html')
    
    def predict(self):
        """Handle prediction request"""
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        location = request.form.get('location', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not self.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, webp'}), 400
        
        temp_filepath = None
        temp_heatmap_path = None
        
        try:
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            # Use WIB timezone (UTC+7)
            wib = timezone(timedelta(hours=7))
            timestamp_dt = datetime.now(wib)
            timestamp = timestamp_dt.strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            temp_filepath = Config.TEMP_FOLDER / filename
            file.save(str(temp_filepath))
            
            # Try to extract GPS from image if location not provided
            gps_data = None
            if not location:
                gps_data = ImageMetadataExtractor.get_gps_data(temp_filepath)
                if gps_data:
                    location = f"GPS: {gps_data['latitude']:.6f}, {gps_data['longitude']:.6f}"
                else:
                    location = "Lokasi tidak diketahui"
            
            # Make prediction
            result = self.model_handler.predict(temp_filepath)
            recommendation = self.model_handler.get_recommendation(
                result['class'],
                result['confidence']
            )
            
            # Upload original image to Cloudinary (if available)
            image_url = None
            heatmap_url = None
            cloudinary_public_id = None
            
            if Config.USE_DATABASE and self.cloudinary:
                try:
                    print(f"☁️ Uploading image to Cloudinary...")
                    upload_result = self.cloudinary.upload_image(
                        str(temp_filepath),
                        folder='waste-detection',
                        public_id=f"detection_{timestamp}"
                    )
                    image_url = upload_result['url']
                    cloudinary_public_id = upload_result['public_id']
                    print(f"✓ Image uploaded: {image_url}")
                except Exception as e:
                    print(f"⚠️ Cloudinary upload failed: {e}")
            
            # Generate heatmap
            heatmap_filename = None
            heatmap_error = None
            try:
                print(f"🔥 Generating heatmap for {filename}...")
                overlay = self.model_handler.generate_gradcam(temp_filepath, result['class_idx'])
                if overlay is not None:
                    heatmap_filename = f"heatmap_{filename}"
                    temp_heatmap_path = Config.TEMP_FOLDER / heatmap_filename
                    Image.fromarray(overlay).save(str(temp_heatmap_path))
                    print(f"✓ Heatmap generated: {heatmap_filename}")
                    
                    # Upload heatmap to Cloudinary (if available)
                    if Config.USE_DATABASE and self.cloudinary and cloudinary_public_id:
                        try:
                            print(f"☁️ Uploading heatmap to Cloudinary...")
                            heatmap_result = self.cloudinary.upload_heatmap(
                                str(temp_heatmap_path),
                                cloudinary_public_id
                            )
                            heatmap_url = heatmap_result['url']
                            print(f"✓ Heatmap uploaded: {heatmap_url}")
                        except Exception as e:
                            print(f"⚠️ Heatmap upload failed: {e}")
                else:
                    heatmap_error = "Heatmap generation returned None"
                    print(f"❌ {heatmap_error}")
            except Exception as e:
                heatmap_error = str(e)
                print(f"❌ Heatmap generation failed: {e}")
                import traceback
                traceback.print_exc()
            
            # Save detection log (database or JSON)
            log_data = {
                'timestamp': timestamp_dt,
                'location': location,
                'gps': gps_data,
                'filename': filename,
                'image_url': image_url or f"/uploads/{filename}",  # Fallback to /uploads route
                'heatmap_url': heatmap_url or (f"/uploads/{heatmap_filename}" if heatmap_filename else None),
                'heatmap_filename': heatmap_filename,
                'prediction': result,
                'recommendation': recommendation,
                'campus': Config.CAMPUS_SHORT
            }
            self._save_detection_log(log_data)
            
            # Cleanup temp files ONLY if uploaded to cloud
            # Keep files in temp folder for localhost viewing
            if Config.USE_DATABASE and image_url:
                try:
                    if temp_filepath and temp_filepath.exists():
                        temp_filepath.unlink()
                    if temp_heatmap_path and temp_heatmap_path.exists():
                        temp_heatmap_path.unlink()
                    print("✓ Temp files cleaned up (uploaded to cloud)")
                except Exception as e:
                    print(f"⚠️ Cleanup error: {e}")
            else:
                print(f"📁 Files kept in temp folder for viewing: {filename}")
            
            # Prepare response
            response = {
                'success': True,
                'filename': filename,
                'image_url': image_url or f"/uploads/{filename}",  # Use /uploads route for localhost
                'heatmap_url': heatmap_url or (f"/uploads/{heatmap_filename}" if heatmap_filename else None),
                'heatmap_filename': heatmap_filename,
                'heatmap_error': heatmap_error,
                'location': location,
                'gps': gps_data,
                'prediction': result,
                'recommendation': recommendation,
                'timestamp': timestamp,
                'campus': Config.CAMPUS_SHORT,
                'using_database': Config.USE_DATABASE
            }
            
            return jsonify(response)
        
        except Exception as e:
            # Cleanup on error
            try:
                if temp_filepath and temp_filepath.exists():
                    temp_filepath.unlink()
                if temp_heatmap_path and temp_heatmap_path.exists():
                    temp_heatmap_path.unlink()
            except:
                pass
            return jsonify({'error': str(e)}), 500
    
    def _save_detection_log(self, log_data):
        """Save detection log to database or JSON file"""
        if Config.USE_DATABASE and self.db:
            # Save to PostgreSQL
            try:
                self.db.add_detection(log_data)
                print("✓ Log saved to database")
            except Exception as e:
                print(f"❌ Database save error: {e}")
                # Fallback to JSON
                self._save_to_json(log_data)
        else:
            # Save to JSON file
            self._save_to_json(log_data)
    
    def _save_to_json(self, log_data):
        """Fallback: Save to JSON file"""
        log_file = Config.LOG_FILE
        
        # Convert datetime to string for JSON
        if isinstance(log_data.get('timestamp'), datetime):
            log_data['timestamp'] = log_data['timestamp'].strftime('%Y%m%d_%H%M%S')
        
        # Load existing logs
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading logs: {e}")
                logs = []
        
        # Append new log
        logs.append(log_data)
        
        # Save logs
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            print(f"✓ Log saved to {log_file}")
        except Exception as e:
            print(f"❌ Error saving log: {e}")
    
    def uploaded_file(self, filename):
        """Serve uploaded files from temp folder"""
        return send_from_directory(Config.TEMP_FOLDER, filename)
    
    def history(self):
        """Show detection history page"""
        return render_template('history.html')
    
    def get_logs(self):
        """Get detection logs from database or JSON"""
        if Config.USE_DATABASE and self.db:
            try:
                logs = self.db.get_all_detections()
                print(f"✓ Loaded {len(logs)} logs from database")
                return jsonify(logs)
            except Exception as e:
                print(f"❌ Database error: {e}")
                # Fallback to JSON
                return self._get_logs_from_json()
        else:
            return self._get_logs_from_json()
    
    def _get_logs_from_json(self):
        """Fallback: Get logs from JSON file"""
        log_file = Config.LOG_FILE
        
        if not log_file.exists():
            print(f"⚠️ Log file not found: {log_file}")
            return jsonify([])
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            print(f"✓ Loaded {len(logs)} logs from {log_file}")
            # Return logs in reverse order (newest first)
            return jsonify(logs[::-1])
        except Exception as e:
            print(f"❌ Error loading logs: {e}")
            return jsonify([])
    
    def campus_map(self):
        """Show campus map page"""
        return render_template('campus_map.html')
    
    def get_map_data(self):
        """Get map data with latest detection per location - ONLY valid locations"""
        if Config.USE_DATABASE and self.db:
            try:
                result = self.db.get_latest_by_location()
                print(f"📊 API returning {len(result)} valid locations from database")
                return jsonify(result)
            except Exception as e:
                print(f"❌ Database error: {e}")
                # Fallback to JSON
                return self._get_map_data_from_json()
        else:
            return self._get_map_data_from_json()
    
    def _get_map_data_from_json(self):
        """Fallback: Get map data from JSON"""
        log_file = Config.LOG_FILE
        
        if not log_file.exists():
            return jsonify([])
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Group by location and get latest detection
            location_map = {}
            for log in reversed(logs):  # Process from newest
                location = log.get('location', '').strip()
                
                # SKIP invalid locations
                if not location or location == 'Lokasi tidak diketahui' or location == 'Unknown':
                    continue
                
                if location not in location_map:
                    location_map[location] = {
                        'location': location,
                        'class': log['prediction']['class'],
                        'confidence': log['prediction']['confidence'],
                        'timestamp': log['timestamp'],
                        'recommendation': log['recommendation']
                    }
            
            result = list(location_map.values())
            print(f"📊 API returning {len(result)} valid locations: {[r['location'] for r in result]}")
            return jsonify(result)
        except Exception as e:
            print(f"Error getting map data: {e}")
            return jsonify([])
    
    def run(self, debug=False, host='127.0.0.1', port=8080):
        """Run the Flask application"""
        print("=" * 60)
        print(f"🚀 Sistem Deteksi Sampah - {Config.CAMPUS_NAME}")
        print("=" * 60)
        print(f"📍 Server: http://localhost:{port}")
        print(f"📁 Model: {Config.MODEL_PATH}")
        print(f"📂 Temp: {Config.TEMP_FOLDER}")
        if Config.USE_DATABASE:
            print(f"💾 Storage: PostgreSQL + Cloudinary")
        else:
            print(f"💾 Storage: JSON file (fallback)")
        print("=" * 60)
        self.app.run(debug=debug, host=host, port=port, use_reloader=False)


# Create app instance for Gunicorn
waste_app = WasteDetectionApp()
app = waste_app.app  # Expose Flask app for Gunicorn

# Application entry point
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))  # Use PORT from env or default 8080
    waste_app.run(debug=False, host='0.0.0.0', port=port)
