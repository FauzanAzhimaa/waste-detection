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
    
    # YOLO Object Detection Model
    YOLO_MODEL_PATH = BASE_DIR / 'models' / 'waste_yolo_best.pt'
    USE_YOLO = True  # Enable/disable object detection
    YOLO_CONFIDENCE = 0.10  # Confidence threshold (lower = more detections, more sensitive)
    
    # Temporary folder for processing (will be deleted after upload to cloud)
    TEMP_FOLDER = BASE_DIR / 'temp'
    
    # Fallback for JSON storage if database not available
    LOG_FILE = BASE_DIR / 'detection_logs.json'
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    IMAGE_SIZE = (224, 224)
    CLASS_NAMES = ['Bersih', 'Tumpukan Parah', 'Tumpukan Ringan']
    
    # Model Performance Metrics (from model_analysis_report.json)
    MODEL_ACCURACY = 40.54  # Overall test accuracy in percentage
    MODEL_STATUS = "PROTOTYPE"  # PROTOTYPE, PRODUCTION, EXPERIMENTAL
    DATASET_SIZE = 236  # Total images used for training
    DATASET_TARGET = 900  # Target dataset size for production
    
    # Per-class accuracy (from confusion matrix analysis)
    CLASS_ACCURACY = {
        'Bersih': 0.0,  # 0% - Model cannot detect clean areas
        'Tumpukan Parah': 100.0,  # 100% - But due to bias (predicts everything as this)
        'Tumpukan Ringan': 0.0  # 0% - Model cannot detect light waste
    }
    
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


class YOLODetector:
    """YOLO object detector for waste detection"""
    
    def __init__(self, model_path, confidence=0.25):
        self.model_path = model_path
        self.confidence = confidence
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model"""
        if not self.model_path.exists():
            print(f"⚠️ YOLO model not found: {self.model_path}")
            print(f"   Object detection will be disabled")
            return
        
        try:
            from ultralytics import YOLO
            self.model = YOLO(str(self.model_path))
            print(f"✓ YOLO model loaded: {self.model_path.name}")
        except Exception as e:
            print(f"❌ Error loading YOLO: {e}")
            self.model = None
    
    def detect(self, image_path):
        """Detect objects in image and return results with bounding boxes"""
        if not self.model:
            return None
        
        try:
            # Run detection
            results = self.model(str(image_path), conf=self.confidence, verbose=False)
            
            if not results or len(results) == 0:
                return None
            
            result = results[0]
            
            # Extract detections (convert numpy to Python native types)
            detections = []
            for box in result.boxes:
                bbox = box.xyxy[0].cpu().numpy().tolist()  # Convert tensor to list
                conf = float(box.conf.cpu().numpy()[0])  # Convert tensor to float
                cls = int(box.cls.cpu().numpy()[0])  # Convert tensor to int
                
                detections.append({
                    'class': result.names[cls],
                    'confidence': conf,
                    'bbox': bbox,  # [x1, y1, x2, y2]
                })
            
            # Get image with bounding boxes drawn (without labels)
            image_with_boxes = result.plot(
                labels=False,  # Hide class labels
                conf=False,    # Hide confidence scores
                line_width=3,  # Thicker boxes
                font_size=0    # No text
            )  # Returns numpy array
            
            return {
                'count': len(detections),
                'detections': detections,
                'image_with_boxes': image_with_boxes  # This will be saved as image, not serialized
            }
        except Exception as e:
            print(f"❌ YOLO detection error: {e}")
            import traceback
            traceback.print_exc()
            return None


class WasteDetectionModel:
    """Model handler for waste detection"""
    
    def __init__(self, model_path, class_names, image_size=(224, 224)):
        self.model_path = model_path
        self.class_names = class_names
        self.image_size = image_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model with TensorFlow workaround for Railway"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        try:
            # Aggressive memory optimization for Railway free tier (512MB)
            import gc
            gc.collect()
            
            # Disable GPU completely to prevent CUDA errors
            import os
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
            
            try:
                tf.config.set_visible_devices([], 'GPU')
                # Limit TensorFlow memory growth
                physical_devices = tf.config.list_physical_devices('CPU')
                if physical_devices:
                    tf.config.experimental.set_memory_growth(physical_devices[0], True)
            except Exception as e:
                print(f"⚠️ GPU config warning (ignored): {e}")
            
            # Load model with minimal memory footprint
            print(f"📦 Loading model from {self.model_path}...")
            print(f"💾 Memory optimization: CPU-only mode")
            
            self.model = tf.keras.models.load_model(
                str(self.model_path), 
                compile=False  # Don't compile to save memory
            )
            
            print(f"✓ Model loaded successfully (CPU mode)")
            
            # Force garbage collection after load
            gc.collect()
            
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
    
    def generate_yolo_density_heatmap(self, image_path, detections):
        """
        Generate density heatmap from YOLO detections
        Shows spatial distribution and clustering of detected waste objects
        
        Args:
            image_path: Path to original image
            detections: List of YOLO detections with bbox coordinates
        
        Returns:
            overlay: RGB image with heatmap overlay
        """
        try:
            print(f"🔥 Generating YOLO density heatmap...")
            
            # Load original image
            img_pil = Image.open(image_path).convert('RGB')
            original_size = img_pil.size
            img_array = np.array(img_pil)
            
            # Create empty heatmap
            heatmap = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=np.float32)
            
            if not detections or len(detections) == 0:
                print("ℹ️ No detections - returning blue (clean) heatmap")
                # Return blue heatmap for clean area
                heatmap_colored = np.zeros_like(img_array)
                heatmap_colored[:, :, 2] = 255  # Blue channel
                overlay = (heatmap_colored * 0.3 + img_array * 0.7).astype(np.uint8)
                return overlay
            
            print(f"📍 Creating density map from {len(detections)} objects...")
            
            # Add heat for each detection
            for det in detections:
                bbox = det['bbox']  # [x1, y1, x2, y2]
                x1, y1, x2, y2 = map(int, bbox)
                
                # Ensure coordinates are within image bounds
                x1 = max(0, min(x1, img_array.shape[1] - 1))
                x2 = max(0, min(x2, img_array.shape[1] - 1))
                y1 = max(0, min(y1, img_array.shape[0] - 1))
                y2 = max(0, min(y2, img_array.shape[0] - 1))
                
                # Add heat to bbox area (higher in center)
                width = x2 - x1
                height = y2 - y1
                
                if width > 0 and height > 0:
                    # Create gaussian-like distribution for smoother heatmap
                    y_coords, x_coords = np.ogrid[0:height, 0:width]
                    center_y, center_x = height / 2, width / 2
                    
                    # Distance from center (normalized)
                    dist = np.sqrt(((x_coords - center_x) / (width / 2)) ** 2 + 
                                   ((y_coords - center_y) / (height / 2)) ** 2)
                    
                    # Gaussian-like weight (higher in center, lower at edges)
                    weight = np.exp(-dist ** 2 / 0.5)
                    
                    # Add weighted heat to heatmap
                    heatmap[y1:y2, x1:x2] += weight
            
            # Apply Gaussian blur for smooth transitions
            kernel_size = max(31, int(min(img_array.shape[:2]) * 0.05))  # 5% of image size
            if kernel_size % 2 == 0:
                kernel_size += 1  # Must be odd
            heatmap = cv2.GaussianBlur(heatmap, (kernel_size, kernel_size), 0)
            
            # Normalize heatmap
            if heatmap.max() > 0:
                heatmap = heatmap / heatmap.max()
            
            # Apply colormap (JET: blue=low, red=high)
            heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
            
            # Create overlay (70% heatmap, 30% original)
            overlay = (heatmap_colored * 0.7 + img_array * 0.3).astype(np.uint8)
            
            print(f"✓ YOLO density heatmap generated (max density: {heatmap.max():.2f})")
            return overlay
            
        except Exception as e:
            print(f"❌ YOLO heatmap error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_gradcam(self, image_path, pred_index=None):
        """
        DEPRECATED: Grad-CAM heatmap (replaced by YOLO density heatmap)
        Kept for backward compatibility but not used
        """
        try:
            print(f"⚠️ Grad-CAM is deprecated - using YOLO density heatmap instead")
            print(f"🔥 Starting Grad-CAM generation...")
            print(f"📊 Model layers: {len(self.model.layers)} total")
            
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
            
            # Find last conv layer - multiple strategies
            target_layer = None
            layer_name = None
            
            # Strategy 1: Try to find specific good layers in MobileNetV2
            # block_16 or block_15 usually give better results than the very last layer
            preferred_layers = ['block_16', 'block_15', 'block_14', 'Conv_1']
            
            for layer in reversed(self.model.layers):
                if hasattr(layer, 'layers'):
                    # It's a nested model (MobileNetV2)
                    for sublayer in reversed(layer.layers):
                        # First try preferred layers
                        for pref in preferred_layers:
                            if pref.lower() in sublayer.name.lower():
                                target_layer = sublayer
                                layer_name = sublayer.name
                                print(f"✓ Found preferred layer: {layer_name}")
                                break
                        if target_layer:
                            break
                        # Fallback to any conv layer
                        if 'conv' in sublayer.name.lower():
                            target_layer = sublayer
                            layer_name = sublayer.name
                            print(f"✓ Found nested conv layer: {layer_name}")
                            break
                    if target_layer:
                        break
            
            # Strategy 2: If not found, try direct model layers
            if not target_layer:
                for layer in reversed(self.model.layers):
                    if 'conv' in layer.__class__.__name__.lower():
                        target_layer = layer
                        layer_name = layer.name
                        print(f"✓ Found direct conv layer: {layer_name}")
                        break
            
            # Strategy 3: Use any layer with output shape (None, H, W, C)
            if not target_layer:
                for layer in reversed(self.model.layers):
                    try:
                        output_shape = layer.output_shape
                        if len(output_shape) == 4:  # (batch, height, width, channels)
                            target_layer = layer
                            layer_name = layer.name
                            print(f"✓ Found 4D output layer: {layer_name}")
                            break
                    except:
                        continue
            
            if not target_layer:
                print("❌ No suitable conv layer found")
                print(f"📋 Available layers: {[l.name for l in self.model.layers[:5]]}...")
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
            
            # Apply threshold to focus on important areas (top 30% activation)
            threshold = np.percentile(heatmap, 70)
            heatmap_focused = np.where(heatmap >= threshold, heatmap, heatmap * 0.3)
            
            # Resize heatmap to original image size
            heatmap_resized = cv2.resize(heatmap_focused, original_size)
            heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
            
            # Create overlay with higher heatmap intensity
            original_array = np.array(img_pil, dtype=np.float32)
            overlay = heatmap_colored * 0.7 + original_array * 0.3
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
        
        # Initialize classification model
        self.model_handler = WasteDetectionModel(
            Config.MODEL_PATH,
            Config.CLASS_NAMES,
            Config.IMAGE_SIZE
        )
        
        # Initialize YOLO detector (object detection)
        self.yolo_detector = None
        if Config.USE_YOLO:
            try:
                self.yolo_detector = YOLODetector(
                    Config.YOLO_MODEL_PATH,
                    Config.YOLO_CONFIDENCE
                )
                if self.yolo_detector.model:
                    print("✓ YOLO object detection enabled")
                else:
                    print("⚠️ YOLO disabled (model not found)")
            except Exception as e:
                print(f"⚠️ YOLO initialization failed: {e}")
                self.yolo_detector = None
        
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
            
            # YOLO Object Detection (run FIRST to get detections for heatmap)
            yolo_result = None
            bbox_filename = None
            bbox_url = None
            temp_bbox_path = None
            yolo_detections = []  # For heatmap generation
            
            if self.yolo_detector and self.yolo_detector.model:
                try:
                    print(f"🎯 Running YOLO object detection...")
                    yolo_result = self.yolo_detector.detect(temp_filepath)
                    
                    if yolo_result and yolo_result['count'] > 0:
                        print(f"✓ YOLO detected {yolo_result['count']} objects")
                        yolo_detections = yolo_result['detections']  # Save for heatmap
                        
                        # Save image with bounding boxes
                        bbox_filename = f"bbox_{filename}"
                        temp_bbox_path = Config.TEMP_FOLDER / bbox_filename
                        Image.fromarray(yolo_result['image_with_boxes']).save(str(temp_bbox_path))
                        print(f"✓ Bounding boxes saved: {bbox_filename}")
                        
                        # Upload bbox image to Cloudinary (if available)
                        if Config.USE_DATABASE and self.cloudinary and cloudinary_public_id:
                            try:
                                print(f"☁️ Uploading bbox image to Cloudinary...")
                                bbox_result = self.cloudinary.upload_image(
                                    str(temp_bbox_path),
                                    folder='waste-detection',
                                    public_id=f"{cloudinary_public_id}_bbox"
                                )
                                bbox_url = bbox_result['url']
                                print(f"✓ Bbox image uploaded: {bbox_url}")
                            except Exception as e:
                                print(f"⚠️ Bbox upload failed: {e}")
                        
                        # Set bbox URL (cloud or local)
                        yolo_result['bbox_image_url'] = bbox_url or f"/uploads/{bbox_filename}"
                    else:
                        print("ℹ️ No objects detected by YOLO (clean area)")
                except Exception as e:
                    print(f"❌ YOLO detection failed: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Generate YOLO-based density heatmap (using YOLO detections)
            heatmap_filename = None
            heatmap_error = None
            try:
                print(f"🔥 Generating YOLO density heatmap for {filename}...")
                overlay = self.model_handler.generate_yolo_density_heatmap(temp_filepath, yolo_detections)
                if overlay is not None:
                    heatmap_filename = f"heatmap_{filename}"
                    temp_heatmap_path = Config.TEMP_FOLDER / heatmap_filename
                    Image.fromarray(overlay).save(str(temp_heatmap_path))
                    print(f"✓ YOLO density heatmap generated: {heatmap_filename}")
                    
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
            # Prepare YOLO data for JSON (exclude numpy array)
            yolo_data_for_log = None
            if yolo_result:
                yolo_data_for_log = {
                    'count': yolo_result['count'],
                    'detections': yolo_result['detections'],
                    'bbox_image_url': yolo_result.get('bbox_image_url')
                }
            
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
                'campus': Config.CAMPUS_SHORT,
                # YOLO detection data (without numpy array)
                'yolo_detection': yolo_data_for_log,
                'object_count': yolo_result['count'] if yolo_result else 0,
                'bbox_image_url': yolo_result.get('bbox_image_url') if yolo_result else None,
                'bbox_filename': bbox_filename,
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
                    if temp_bbox_path and temp_bbox_path.exists():
                        temp_bbox_path.unlink()
                    print("✓ Temp files cleaned up (uploaded to cloud)")
                except Exception as e:
                    print(f"⚠️ Cleanup error: {e}")
            else:
                print(f"📁 Files kept in temp folder for viewing: {filename}")
            
            # Get prediction confidence and determine reliability
            predicted_class = result['class']
            confidence = result['confidence']
            
            # YOLO-BASED OVERRIDE: Use YOLO detection with spatial analysis
            yolo_override = None
            yolo_based_class = None
            if yolo_result and yolo_result['count'] is not None:
                object_count = yolo_result['count']
                
                if object_count == 0:
                    yolo_based_class = 'Bersih'
                    yolo_override = f'✅ YOLO mendeteksi 0 objek sampah → Area Bersih'
                else:
                    # Analyze spatial clustering: are objects piled up or scattered?
                    detections = yolo_data_for_log.get('detections', []) if yolo_data_for_log else []
                    is_piled = self._analyze_pile_clustering(detections)
                    
                    # Improved classification logic:
                    # 1. If piled (high density/close proximity) → PARAH regardless of count
                    # 2. If many objects (>8) even if scattered → PARAH (too much waste)
                    # 3. If moderate (3-8 scattered) → RINGAN
                    # 4. If few (1-2 scattered) → RINGAN with warning
                    
                    if is_piled:
                        # Objects are close together (piled up) → always severe
                        yolo_based_class = 'Tumpukan Parah'
                        yolo_override = f'🚨 YOLO: {object_count} objek MENUMPUK (kepadatan tinggi) → Tumpukan Parah'
                    elif object_count > 8:
                        # Too many objects even if scattered → severe
                        yolo_based_class = 'Tumpukan Parah'
                        yolo_override = f'🚨 YOLO: {object_count} objek sampah (terlalu banyak) → Tumpukan Parah'
                    elif object_count >= 3:
                        # Moderate scattered objects → light
                        yolo_based_class = 'Tumpukan Ringan'
                        yolo_override = f'⚠️ YOLO: {object_count} objek sampah berserakan → Tumpukan Ringan'
                    else:
                        # Few scattered objects (1-2) → light with warning
                        yolo_based_class = 'Tumpukan Ringan'
                        yolo_override = f'⚠️ YOLO: {object_count} objek sampah → Tumpukan Ringan'
                        if object_count <= 2:
                            yolo_override += ' (⚠️ Mungkin ada objek kecil tidak terdeteksi)'
                
                # Override recommendation AND prediction with YOLO-based classification
                if yolo_based_class:
                    # Update prediction result to use YOLO-based class
                    result['class'] = yolo_based_class
                    result['confidence'] = 0.95  # High confidence for YOLO
                    result['yolo_override'] = True
                    
                    # Update probabilities to reflect YOLO-based classification
                    result['probabilities'] = {
                        'Bersih': 0.95 if yolo_based_class == 'Bersih' else 0.02,
                        'Tumpukan Ringan': 0.95 if yolo_based_class == 'Tumpukan Ringan' else 0.02,
                        'Tumpukan Parah': 0.95 if yolo_based_class == 'Tumpukan Parah' else 0.01
                    }
                    
                    predicted_class = yolo_based_class
                    confidence = 0.95  # High confidence for YOLO
                    
                    recommendation = self.model_handler.get_recommendation(yolo_based_class, 0.95)
                    print(f"🎯 YOLO Override: Classification → {yolo_based_class} ({object_count} objects, piled={is_piled if object_count > 0 else False})")
            
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
                'using_database': Config.USE_DATABASE,
                # YOLO object detection results (without numpy array)
                'yolo_detection': yolo_data_for_log,
                'object_count': yolo_result['count'] if yolo_result else 0,
                'bbox_image_url': yolo_result.get('bbox_image_url') if yolo_result else None
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
    
    def _analyze_pile_clustering(self, detections):
        """
        Analyze if detected objects are piled up (close together) or scattered
        Returns True if objects are piled up, False if scattered
        
        Improved logic:
        - Consider object count (more objects = potentially more severe)
        - Consider density (objects in small area = piled)
        - Consider overlap and proximity
        """
        if not detections:
            return False
        
        object_count = len(detections)
        
        # Single object is never "piled"
        if object_count == 1:
            return False
        
        # Calculate center points and bbox sizes
        centers = []
        total_area = 0
        for det in detections:
            bbox = det['bbox']  # [x1, y1, x2, y2]
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            centers.append((center_x, center_y))
            
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            total_area += width * height
        
        # Calculate bounding box that contains all objects
        all_x = [c[0] for c in centers]
        all_y = [c[1] for c in centers]
        spread_x = max(all_x) - min(all_x)
        spread_y = max(all_y) - min(all_y)
        spread_area = spread_x * spread_y if spread_x > 0 and spread_y > 0 else 1
        
        # Calculate density: total object area / spread area
        density = total_area / spread_area if spread_area > 0 else 0
        
        # Calculate average distance between nearest neighbors
        min_distances = []
        for i in range(len(centers)):
            min_dist = float('inf')
            for j in range(len(centers)):
                if i != j:
                    x1, y1 = centers[i]
                    x2, y2 = centers[j]
                    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    min_dist = min(min_dist, distance)
            if min_dist != float('inf'):
                min_distances.append(min_dist)
        
        avg_min_distance = sum(min_distances) / len(min_distances) if min_distances else 0
        
        # Calculate average bbox size for normalization
        avg_bbox_size = (total_area / object_count) ** 0.5  # sqrt of average area
        normalized_distance = avg_min_distance / avg_bbox_size if avg_bbox_size > 0 else avg_min_distance
        
        # Decision logic:
        # 1. High density (>0.3) = objects occupy significant portion of spread area = PILED
        # 2. Close proximity (normalized distance < 2.5) = objects very close = PILED
        # 3. Many objects (>10) with moderate density (>0.15) = PILED
        is_piled = (
            density > 0.3 or  # High density
            normalized_distance < 2.5 or  # Very close objects
            (object_count > 10 and density > 0.15)  # Many objects with moderate density
        )
        
        print(f"📏 Clustering: count={object_count}, density={density:.3f}, norm_dist={normalized_distance:.2f} → {'PILED' if is_piled else 'SCATTERED'}")
        return is_piled
    
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
        """Fallback: Get map data from JSON - Show ALL detections per location"""
        log_file = Config.LOG_FILE
        
        if not log_file.exists():
            return jsonify([])
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Group by location and collect ALL detections
            location_map = {}
            for log in reversed(logs):  # Process from newest
                location = log.get('location', '').strip()
                
                # SKIP invalid locations
                if not location or location == 'Lokasi tidak diketahui' or location == 'Unknown':
                    continue
                
                # Add to location group (keep all detections)
                if location not in location_map:
                    location_map[location] = []
                
                location_map[location].append({
                    'location': location,
                    'class': log['prediction']['class'],
                    'confidence': log['prediction']['confidence'],
                    'timestamp': log['timestamp'],
                    'recommendation': log['recommendation'],
                    'image_url': log.get('image_url', ''),
                    'heatmap_url': log.get('heatmap_url', ''),
                    'bbox_image_url': log.get('bbox_image_url', ''),
                    'object_count': log.get('object_count', 0),
                })
            
            # Flatten to list (all detections)
            result = []
            for location, detections in location_map.items():
                result.extend(detections)
            
            print(f"📊 API returning {len(result)} total detections from {len(location_map)} locations")
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
