import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
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
        self.history = self.model.fit(
            self.train_dataset,
            epochs=self.config.params_epoch,
            validation_data=self.validation_dataset,
            callbacks = callback_list
        )

        self.save_model(
            model = self.model,
            model_path = self.config.trained_model_path
        )
    
    def plot_and_save_history(self):
    # Extracting loss and accuracy from history
        history_dict = self.history.history
        train_loss = history_dict['loss']
        val_loss = history_dict['val_loss']
        train_acc = history_dict['accuracy']
        val_acc = history_dict['val_accuracy']

        epochs = range(1, len(train_loss) + 1)

        # Plotting training and validation loss
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(epochs, train_loss, label='Training Loss')
        plt.plot(epochs, val_loss, label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        # Plotting training and validation accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, train_acc, label='Training Accuracy')
        plt.plot(epochs, val_acc, label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        # Saving plots
        plt.savefig(self.config.result_image_path)

        plt.close()
    
    def plot_validation_images_with_predictions(self):
        # Take 16 images from the validation dataset
        # Label mapping
        label_map = {0: 'Pizza', 1: 'Steak'}

        # Take 16 images from the validation dataset
        images, labels = next(iter(self.validation_dataset.take(1)))
        images, labels = images[:16], labels[:16]

        # Predict labels
        predicted_labels = self.model.predict(images)
        res = ["Steak" if label >= 0 else "Pizza" for label in predicted_labels]

        # Plotting
        plt.figure(figsize=(16, 16))
        for i in range(16):
            plt.subplot(4, 4, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            true_label = label_map[labels[i].numpy()]
            plt.title(f"True: {true_label}\nPredicted: {res[i]}")
            plt.axis("off")

        # Saving the plot
        plt.savefig(self.config.evaluation_pictures)

        # Close the plot to avoid displaying
        plt.close()