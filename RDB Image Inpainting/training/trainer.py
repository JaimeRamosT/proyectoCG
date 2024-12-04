# training/trainer.py
import tensorflow as tf
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import logging
from models.inpainting import build_functional_model


# training/trainer.py
class ModelTrainer:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_callbacks(self):
        return [
            EarlyStopping(
                monitor='loss',
                patience=self.config['early_stopping_patience'],
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor='loss',
                factor=self.config['lr_reduce_factor'],
                patience=self.config['lr_reduce_patience']
            )
        ]

    def train(self, model, dataset):
        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=self.config['learning_rate']
            ),
            loss=custom_loss
        )

        history = model.fit(
            dataset,
            epochs=self.config['epochs'],
            callbacks=self.create_callbacks()
        )

        if self.config['save_path']:
            # Convert to functional model for HDF5 saving
            functional_model = build_functional_model(
                num_channels=model.num_channels,
                num_rdbs=len(model.rdbs),
                layers_per_rdb=model.rdbs[0].layers
            )
            # Copy weights
            functional_model.set_weights(model.get_weights())
            # Save as HDF5
            functional_model.save(self.config['save_path'], save_format='h5')
            self.logger.info(f"Model saved to {self.config['save_path']}")

        return model

def custom_loss(y_true, y_pred):
    #Pérdida de reconstrucción + pérdida de validación de máscara
    reconstruction_loss = tf.keras.losses.mean_squared_error(y_true, y_pred)
    
    #Pérdida adicional para validar la reconstrucción de áreas enmascaradas
    mask_loss = tf.reduce_mean(tf.abs(y_true - y_pred))
    
    return reconstruction_loss + 0.1 * mask_loss