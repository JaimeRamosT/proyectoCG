# data/dataset.py
import tensorflow as tf
from keras.utils import image_dataset_from_directory

def create_mask(image):
    mask = tf.random.uniform(tf.shape(image), minval=0, maxval=2, dtype=tf.int32)
    mask = tf.cast(mask, tf.float32)
    masked_image = image * mask
    return tf.concat([masked_image, mask], axis=-1), image

def load_and_preprocess_dataset(directory, image_size=(256, 256), batch_size=32):
    dataset = image_dataset_from_directory(
        directory,
        image_size=image_size,
        batch_size=batch_size,
        label_mode=None,
        shuffle=True
    )
    dataset = dataset.map(lambda x: x / 255.0)
    dataset = dataset.map(create_mask)
    return dataset