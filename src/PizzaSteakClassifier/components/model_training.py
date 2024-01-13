import tensorflow as tf
from pathlib import Path
from PizzaSteakClassifier.entity.config_entity import TrainingConfig

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.update_base_model_path
        )
    
    def data_preparation(self):
        config = self.config

        train_dataset = tf.keras.utils.image_dataset_from_directory(
            str(config.training_data),
            validation_split=config.params_validation_split,
            subset="training",
            seed=123,
            image_size=config.params_image_size[:-1],
            batch_size=config.params_batch_size
        )

        validation_dataset = tf.keras.utils.image_dataset_from_directory(
            str(config.training_data),
            validation_split=config.params_validation_split,
            subset="validation",
            seed=123,
            image_size=config.params_image_size[:-1],
            batch_size=config.params_batch_size
        )

        val_batches = tf.data.experimental.cardinality(validation_dataset)
        test_dataset = validation_dataset.take(val_batches // 5)
        validation_dataset = validation_dataset.skip(val_batches // 5)

        AUTOTUNE = tf.data.AUTOTUNE

        self.train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
        self.validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
        self.test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    @staticmethod
    def save_model(model: tf.keras.Model, model_path: Path):
        model.save(model_path)
    
    def train(self, callback_list: list):
        self.model.fit(
            self.train_dataset,
            epochs=self.config.params_epoch,
            validation_data=self.validation_dataset,
            callbacks = callback_list
        )

        self.save_model(
            model = self.model,
            model_path = self.config.trained_model_path
        )