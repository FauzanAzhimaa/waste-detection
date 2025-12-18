"""
Cloudinary helper for image upload and management
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from pathlib import Path


class CloudinaryManager:
    """Manage image uploads to Cloudinary"""
    
    def __init__(self):
        """Initialize Cloudinary configuration"""
        self.cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        self.api_key = os.environ.get('CLOUDINARY_API_KEY')
        self.api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        if not all([self.cloud_name, self.api_key, self.api_secret]):
            raise ValueError("Cloudinary credentials not found in environment variables")
        
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True
        )
        
        print(f"✓ Cloudinary configured: {self.cloud_name}")
    
    def upload_image(self, file_path, folder='waste-detection', public_id=None):
        """
        Upload image to Cloudinary
        
        Args:
            file_path: Path to image file
            folder: Cloudinary folder name
            public_id: Custom public ID (optional)
        
        Returns:
            dict: Upload result with URL
        """
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type='image',
                overwrite=True,
                transformation=[
                    {'quality': 'auto:good'},
                    {'fetch_format': 'auto'}
                ]
            )
            
            print(f"✓ Image uploaded to Cloudinary: {result['public_id']}")
            
            return {
                'url': result['secure_url'],
                'public_id': result['public_id'],
                'width': result['width'],
                'height': result['height'],
                'format': result['format'],
                'bytes': result['bytes']
            }
        
        except Exception as e:
            print(f"❌ Cloudinary upload error: {e}")
            raise
    
    def upload_heatmap(self, file_path, original_public_id):
        """
        Upload heatmap image to Cloudinary
        
        Args:
            file_path: Path to heatmap file
            original_public_id: Public ID of original image
        
        Returns:
            dict: Upload result with URL
        """
        # Create heatmap public_id based on original
        heatmap_id = f"{original_public_id}_heatmap"
        
        return self.upload_image(
            file_path,
            folder='waste-detection/heatmaps',
            public_id=heatmap_id
        )
    
    def delete_image(self, public_id):
        """Delete image from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            print(f"✓ Image deleted from Cloudinary: {public_id}")
            return result
        except Exception as e:
            print(f"❌ Cloudinary delete error: {e}")
            return None
    
    def get_image_url(self, public_id, transformation=None):
        """
        Get Cloudinary URL for image
        
        Args:
            public_id: Cloudinary public ID
            transformation: Optional transformation dict
        
        Returns:
            str: Image URL
        """
        if transformation:
            return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
        return cloudinary.CloudinaryImage(public_id).build_url()
    
    def get_optimized_url(self, public_id, width=None, height=None):
        """Get optimized image URL with auto format and quality"""
        transformation = {
            'quality': 'auto:good',
            'fetch_format': 'auto'
        }
        
        if width:
            transformation['width'] = width
        if height:
            transformation['height'] = height
        
        return self.get_image_url(public_id, transformation)
