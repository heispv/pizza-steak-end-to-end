import os
import time
import tensorflow as tf
from PizzaSteakClassifier.entity.config_entity import PrepareCallbackConfig

class PrepareCallback:
    def __init__(self, config: PrepareCallbackConfig):
        self.config = config
    
    @property
    def create_tb_callback(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        tb_running_log_dir = os.path.join(
            self.config.tensorboard_log_dir,
            f"tb_logs_{timestamp}"
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)
    
    @property
    def create_ckpt_callback(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=str(self.config.checkpoint_dir), #str is required for ModelCheckpoint
            save_best_only=True
        )
    
    def get_tb_ckpt_callbacks(self):
        return [
                self.create_tb_callback,
                self.create_ckpt_callback
        ]