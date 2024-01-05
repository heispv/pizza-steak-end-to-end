import tensorflow as tf
from pathlib import Path
from PizzaSteakClassifier.entity.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
    
    def download_base_model(self):
        self.model = tf.keras.applications.EfficientNetB0(include_top = self.config.params_include_top,
                                                          weights = self.config.params_weights,
                                                          classes = self.config.params_classes)
        self.save_base_model(path = self.config.base_model_path,
                             model = self.model)
    
    def prepare_full_model(self):
        base_model = self.model
        base_model.trainable = False
        input_shape = tuple(self.config.params_image_size)
        num_classes = self.config.params_classes
        learning_rate = self.config.params_learning_rate


        input_layer = tf.keras.layers.Input(shape = input_shape)
        x = base_model(input_layer, training = False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(units=20, activation = 'relu')(x)
        output_layer = tf.keras.layers.Dense(units = num_classes, activation = 'softmax')(x)
        

        full_model = tf.keras.Model(input_layer, output_layer)

        full_model.compile(
            optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate),
            loss = tf.keras.losses.categorical_crossentropy,
            metrics = ['accuracy']
        )

        return full_model
    
    @staticmethod
    def save_base_model(path: Path, model: tf.keras.models.Model):
        model.save(path)
    
    def update_base_model(self):
        self.full_model = self.prepare_full_model()
        self.save_base_model(path = self.config.updated_base_model_path,
                             model = self.full_model)
