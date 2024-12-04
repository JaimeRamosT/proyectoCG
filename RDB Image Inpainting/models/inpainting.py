import tensorflow as tf
import keras
from keras.layers import Conv2D, Add, Concatenate, Layer, Input, Multiply, Lambda
from keras.utils import image_dataset_from_directory


class PConv2D(Layer):
    def __init__(self, filters, kernel_size, **kwargs):
        super(PConv2D, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
    
    def build(self, input_shape):
        self.conv = Conv2D(
            filters=self.filters, 
            kernel_size=self.kernel_size, 
            padding='same', 
            use_bias=False
        )
        super(PConv2D, self).build(input_shape)
    
    def call(self, inputs):
        #Separar imagen y máscara
        image = inputs[..., :3]  # Imagen RGB
        mask = inputs[..., 3:]   # Máscara de un canal
        
        #Convertir máscara a un solo canal
        mask = tf.reduce_max(mask, axis=-1, keepdims=True)
        
        #Crear kernel para contar píxeles válidos
        valid_kernel = tf.ones(
            (self.kernel_size, self.kernel_size, 1, 1), 
            dtype=mask.dtype
        )
        
        #Contar píxeles válidos en cada ventana
        valid_pixels_count = tf.nn.conv2d(
            mask, 
            valid_kernel, 
            strides=[1, 1, 1, 1], 
            padding='SAME'
        )
        
        #Aplicar máscara a la imagen
        masked_image = image * mask
        
        #Convolución de la imagen enmascarada
        conv_image = self.conv(masked_image)
        
        #Factor de normalización
        #total_kernel_area / pixels_validos
        normalization_factor = tf.math.divide_no_nan(
            tf.cast(tf.size(valid_kernel), image.dtype),
            tf.cast(valid_pixels_count, image.dtype)
        )
        
        #Aplicar normalización
        normalized_conv = conv_image * normalization_factor
        
        #Nueva máscara: donde hay al menos un píxel válido
        new_mask = tf.cast(valid_pixels_count > 0, mask.dtype)
        
        #Concatenar imagen normalizada y nueva máscara
        return tf.concat([normalized_conv, new_mask], axis=-1)
    

class ResidualDenseBlock(Layer):
    def __init__(self, layers, **kwargs):
        super(ResidualDenseBlock, self).__init__(**kwargs)
        self.layers = layers

    def build(self, input_shape):
        self.num_channels = input_shape[-1] - 1  #3 canales de imagen + 1 canal de máscara
        self.partial_convs = [
            PConv2D(filters=self.num_channels, kernel_size=3) 
            for _ in range(self.layers)
        ]
        self.final_conv = PConv2D(filters=self.num_channels, kernel_size=1)

    def call(self, inputs):
        #Separar imagen y máscara del input concatenado
        image = inputs[..., :self.num_channels]
        mask = inputs[..., self.num_channels:]
        
        #Concatenar imagen y máscara para el primer output
        current = tf.concat([image, mask], axis=-1)
        outputs = [current]
        
        for partial_conv in self.partial_convs:
            #Extraer imágenes y máscaras de outputs anteriores
            prev_outputs_img = [out[..., :self.num_channels] for out in outputs]
            prev_outputs_mask = [out[..., self.num_channels:] for out in outputs]
            
            #Concatenar features previas
            concat_image = tf.concat(prev_outputs_img, axis=-1)
            concat_mask = tf.concat(prev_outputs_mask, axis=-1)
            
            #Aplicar convolución parcial
            current = partial_conv(tf.concat([concat_image, concat_mask], axis=-1))
            outputs.append(current)
        
        #Concatenar todas las salidas
        final_features = tf.concat([out[..., :self.num_channels] for out in outputs], axis=-1)
        final_masks = tf.concat([out[..., self.num_channels:] for out in outputs], axis=-1)
        
        #Convolución final
        final_output = self.final_conv(tf.concat([final_features, final_masks], axis=-1))
        
        #Extraer imagen final y añadir conexión residual
        final_image = final_output[..., :self.num_channels] + image
        final_mask = final_output[..., self.num_channels:]
        
        return tf.concat([final_image, final_mask], axis=-1)

class InpaintingRDN(keras.Model):
    def __init__(self, num_channels, num_rdbs=3, layers_per_rdb=3, **kwargs):
        super(InpaintingRDN, self).__init__(**kwargs)
        
        self.num_channels = num_channels
        self.initial_conv1 = PConv2D(64, 5)
        self.initial_conv2 = PConv2D(64, 3)
        self.rdbs = [ResidualDenseBlock(layers=layers_per_rdb) for _ in range(num_rdbs)]
        self.global_fusion_conv1 = PConv2D(64, 1)
        self.global_fusion_conv2 = PConv2D(64, 3)
        self.reconstruction_conv = Conv2D(num_channels, 3, padding='same', activation='sigmoid')

    def call(self, inputs):
        #El input debe ser un tensor concatenado de imagen y máscara
        x = inputs
        
        x = self.initial_conv1(x)
        x = self.initial_conv2(x)
        
        rdb_outputs = []
        for rdb in self.rdbs:
            x = rdb(x)
            #Extraer solo la parte de la imagen para los outputs
            rdb_outputs.append(x[..., :self.num_channels])
        
        gff_input = Concatenate(axis=-1)(rdb_outputs)
        #Crear máscara temporal para las capas finales
        temp_mask = tf.ones_like(gff_input)[..., :self.num_channels]
        gff_output = self.global_fusion_conv1(tf.concat([gff_input, temp_mask], axis=-1))
        gff_output = self.global_fusion_conv2(gff_output)
        
        #Usar solo la parte de la imagen para la reconstrucción final
        output = self.reconstruction_conv(gff_output[..., :self.num_channels])
        
        return output

def create_inpainting_model(num_channels):
    return InpaintingRDN(num_channels)

def build_functional_model(num_channels=3, num_rdbs=3, layers_per_rdb=3):
    inputs = Input(shape=(None, None, num_channels + 1))  # RGB + mask
    
    # Create functional model using InpaintingRDN architecture
    x = inputs
    model = InpaintingRDN(num_channels, num_rdbs, layers_per_rdb)
    outputs = model(x)
    
    return keras.Model(inputs=inputs, outputs=outputs)