# src/gradcam.py
"""
Grad-CAM implementation untuk visualisasi area deteksi sampah pada gambar
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
import cv2

def get_gradcam_heatmap(model, img_array, last_conv_layer_name=None, pred_index=None):
    """
    Generate Grad-CAM heatmap untuk visualisasi area yang dideteksi model
    
    Args:
        model: Trained Keras model
        img_array: Preprocessed image array (1, H, W, 3)
        last_conv_layer_name: Nama layer konvolusi terakhir (auto-detect jika None)
        pred_index: Index kelas untuk visualisasi (auto-detect jika None)
    
    Returns:
        heatmap: Normalized heatmap array
    """
    # Auto-detect last conv layer jika tidak dispesifikasi
    if last_conv_layer_name is None:
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:  # Conv layer has 4D output
                last_conv_layer_name = layer.name
                break
    
    # Buat model untuk Grad-CAM
    grad_model = Model(
        inputs=model.input,
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Compute gradients
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]
    
    # Gradient dari output terhadap feature map
    grads = tape.gradient(class_channel, conv_outputs)
    
    # Global average pooling gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Weight feature maps dengan gradients
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def overlay_gradcam(original_img, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap pada gambar original
    
    Args:
        original_img: Original image (H, W, 3) dalam range 0-255
        heatmap: Grad-CAM heatmap
        alpha: Transparansi overlay
        colormap: OpenCV colormap
    
    Returns:
        superimposed_img: Image dengan heatmap overlay
    """
    # Resize heatmap ke ukuran gambar
    heatmap_resized = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    
    # Convert ke colormap
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    # Overlay
    superimposed = heatmap_colored * alpha + original_img * (1 - alpha)
    superimposed = np.clip(superimposed, 0, 255).astype(np.uint8)
    
    return superimposed, heatmap_resized

def generate_gradcam_visualization(model, img_pil, image_size=(224, 224)):
    """
    Generate complete Grad-CAM visualization dari PIL Image
    
    Args:
        model: Trained model
        img_pil: PIL Image
        image_size: Target size untuk model
    
    Returns:
        dict dengan original, heatmap, overlay, dan prediction info
    """
    # Preprocess image
    img_resized = img_pil.resize(image_size)
    img_array = np.array(img_resized) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    
    # Get prediction
    predictions = model.predict(img_batch, verbose=0)[0]
    pred_idx = int(np.argmax(predictions))
    confidence = float(predictions[pred_idx])
    
    # Generate heatmap
    heatmap = get_gradcam_heatmap(model, img_batch, pred_index=pred_idx)
    
    # Create overlay
    original_array = np.array(img_resized)
    overlay, heatmap_resized = overlay_gradcam(original_array, heatmap)
    
    return {
        'original': original_array,
        'heatmap': heatmap_resized,
        'overlay': overlay,
        'pred_index': pred_idx,
        'confidence': confidence,
        'all_predictions': predictions
    }
