"""
Database models and connection for waste detection system
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone, timedelta
import os

Base = declarative_base()


class Detection(Base):
    """Detection log model"""
    __tablename__ = 'detections'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone(timedelta(hours=7))))
    location = Column(String(255), nullable=False)
    
    # GPS coordinates
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    
    # Image URLs (Cloudinary)
    image_url = Column(Text, nullable=False)
    heatmap_url = Column(Text, nullable=True)
    
    # Prediction results
    predicted_class = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON, nullable=False)
    
    # Recommendation
    recommendation = Column(JSON, nullable=False)
    
    # Metadata
    filename = Column(String(255), nullable=False)
    campus = Column(String(255), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y%m%d_%H%M%S'),
            'location': self.location,
            'gps': {
                'latitude': self.gps_latitude,
                'longitude': self.gps_longitude
            } if self.gps_latitude and self.gps_longitude else None,
            'filename': self.filename,
            'image_url': self.image_url,
            'heatmap_url': self.heatmap_url,
            'prediction': {
                'class': self.predicted_class,
                'confidence': self.confidence,
                'probabilities': self.probabilities,
            },
            'recommendation': self.recommendation,
            'campus': self.campus
        }


class DatabaseManager:
    """Database connection and session manager"""
    
    def __init__(self, database_url=None):
        """Initialize database connection"""
        if database_url is None:
            database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Fix for Railway PostgreSQL URL (postgres:// -> postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Add SSL mode for Railway PostgreSQL
        connect_args = {}
        if 'railway.app' in database_url or 'railway' in database_url:
            connect_args = {
                "sslmode": "require",
                "connect_timeout": 10
            }
        
        self.engine = create_engine(
            database_url, 
            echo=False,
            connect_args=connect_args,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600    # Recycle connections after 1 hour
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        try:
            Base.metadata.create_all(self.engine)
            print("✓ Database connected and tables created")
        except Exception as e:
            print(f"⚠️ Database connection error: {e}")
            raise
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def add_detection(self, detection_data):
        """Add new detection to database"""
        session = self.get_session()
        try:
            detection = Detection(
                timestamp=detection_data.get('timestamp'),
                location=detection_data.get('location'),
                gps_latitude=detection_data.get('gps', {}).get('latitude') if detection_data.get('gps') else None,
                gps_longitude=detection_data.get('gps', {}).get('longitude') if detection_data.get('gps') else None,
                image_url=detection_data.get('image_url'),
                heatmap_url=detection_data.get('heatmap_url'),
                predicted_class=detection_data.get('prediction', {}).get('class'),
                confidence=detection_data.get('prediction', {}).get('confidence'),
                probabilities=detection_data.get('prediction', {}).get('probabilities'),
                recommendation=detection_data.get('recommendation'),
                filename=detection_data.get('filename'),
                campus=detection_data.get('campus')
            )
            session.add(detection)
            session.commit()
            print(f"✓ Detection saved to database: {detection.id}")
            return detection.id
        except Exception as e:
            session.rollback()
            print(f"❌ Error saving detection: {e}")
            raise
        finally:
            session.close()
    
    def get_all_detections(self, limit=None):
        """Get all detections, newest first"""
        session = self.get_session()
        try:
            query = session.query(Detection).order_by(Detection.timestamp.desc())
            if limit:
                query = query.limit(limit)
            detections = query.all()
            return [d.to_dict() for d in detections]
        finally:
            session.close()
    
    def get_detections_by_location(self, location):
        """Get detections for specific location"""
        session = self.get_session()
        try:
            detections = session.query(Detection).filter(
                Detection.location == location
            ).order_by(Detection.timestamp.desc()).all()
            return [d.to_dict() for d in detections]
        finally:
            session.close()
    
    def get_latest_by_location(self):
        """Get latest detection per location for map"""
        session = self.get_session()
        try:
            # Get unique locations
            locations = session.query(Detection.location).distinct().all()
            result = []
            
            for (location,) in locations:
                if location and location != 'Lokasi tidak diketahui':
                    latest = session.query(Detection).filter(
                        Detection.location == location
                    ).order_by(Detection.timestamp.desc()).first()
                    
                    if latest:
                        result.append({
                            'location': latest.location,
                            'class': latest.predicted_class,
                            'confidence': latest.confidence,
                            'timestamp': latest.timestamp.strftime('%Y%m%d_%H%M%S'),
                            'recommendation': latest.recommendation
                        })
            
            return result
        finally:
            session.close()
    
    def get_statistics(self):
        """Get detection statistics"""
        session = self.get_session()
        try:
            total = session.query(Detection).count()
            clean = session.query(Detection).filter(Detection.predicted_class == 'Bersih').count()
            light = session.query(Detection).filter(Detection.predicted_class == 'Tumpukan Ringan').count()
            severe = session.query(Detection).filter(Detection.predicted_class == 'Tumpukan Parah').count()
            
            return {
                'total': total,
                'clean': clean,
                'light': light,
                'severe': severe
            }
        finally:
            session.close()
