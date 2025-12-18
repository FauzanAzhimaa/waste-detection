# src/train.py
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import matplotlib.pyplot as plt

# ========== CONFIG ==========
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Project root
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
NUM_CLASSES = 3
EPOCHS_STAGE1 = 10
EPOCHS_STAGE2 = 10
MODEL_OUT = os.path.join(BASE_DIR, '..', 'models', 'waste_mobilenet.h5')
# ==========================

def build_model(num_classes=NUM_CLASSES, input_shape=(224,224,3)):
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    base.trainable = False
    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    out = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs=base.input, outputs=out)
    return model, base

def get_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.05,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'train'),
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    val_gen = val_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'val'),
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    return train_gen, val_gen

def plot_history(history, out_path=os.path.join(BASE_DIR, '..', 'outputs', 'training_plot.png')):
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.legend(); plt.title('Accuracy')
    plt.subplot(1,2,2)
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend(); plt.title('Loss')
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=200)
    print('Saved training plot to', out_path)

def main():
    model, base = build_model()
    train_gen, val_gen = get_generators()

    # Callbacks
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    checkpoint = ModelCheckpoint(MODEL_OUT, monitor='val_loss', save_best_only=True, verbose=1)
    early = EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)

    # Stage 1: train head
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS_STAGE1,
        callbacks=[checkpoint, early, reduce_lr]
    )
    # Stage 2: fine-tune last layers
    base.trainable = True
    # optionally freeze earlier layers:
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history2 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS_STAGE2,
        callbacks=[checkpoint, early, reduce_lr]
    )

    # combine histories
    history = {}
    for k in history1.history.keys():
        history[k] = history1.history[k] + history2.history.get(k, [])
    # try to plot using last history2 (simpler)
    plot_history(history2)

    # Generate training datasheet
    from training_datasheet import generate_training_datasheet
    print('\nGenerating training datasheet...')
    generate_training_datasheet(history=history, model=model)

    print('Training finished. Best model saved to', MODEL_OUT)

if __name__ == '__main__':
    main()
