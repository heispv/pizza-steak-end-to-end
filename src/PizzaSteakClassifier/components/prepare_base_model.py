import tensorflow as tf
from pathlib import Path
from PizzaSteakClassifier.entity.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
    
    def download_base_model(self):
        self.model = tf.keras.applications.MobileNetV2(input_shape=tuple(self.config.params_image_size),
                                                       include_top=self.config.params_include_top,
                                                       weights=self.config.params_weights)
        self.save_base_model(path = self.config.base_model_path,
                             model = self.model)
    
    
    
    def prepare_full_model(self):
        base_model = self.model
        base_model.trainable = False
        
        data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.2),
        ])

        preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

        # image_batch, label_batch = next(iter(self.train_dataset))
        # feature_batch = base_model(image_batch)

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        # feature_batch_average = global_average_layer(feature_batch)

        # rescale = tf.keras.layers.Rescaling(1./127.5, offset=-1)

        prediction_layer = tf.keras.layers.Dense(1)
        # prediction_batch = prediction_layer(feature_batch_average)

        inputs = tf.keras.Input(shape=(160, 160, 3))
        x = data_augmentation(inputs)
        x = preprocess_input(x)
        x = base_model(x, training=False)
        x = global_average_layer(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        outputs = prediction_layer(x)
        full_model = tf.keras.Model(inputs, outputs)

        full_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.params_learning_rate),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0, name='accuracy')]
        )

        full_model.summary()

        return full_model
    
    @staticmethod
    def save_base_model(path: Path, model: tf.keras.models.Model):
        model.save(path)
    
    def update_base_model(self):
        self.full_model = self.prepare_full_model()
        self.save_base_model(path = self.config.updated_base_model_path,
                             model = self.full_model)
