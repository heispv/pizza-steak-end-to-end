from PizzaSteakClassifier.constants import *
from PizzaSteakClassifier.utils.common import read_yaml_file, create_directories
from PizzaSteakClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, PrepareCallbackConfig

class ConfigurationManager:
    def __init__(
            self,
            config_file_path = CONFIG_FILE_PATH,
            params_file_path = PARAMS_FILE_PATH):
        
        self.config = read_yaml_file(config_file_path)
        self.params = read_yaml_file(params_file_path)

        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = Path(config.root_dir),
            source_url = str(config.source_url),
            local_data_file = Path(config.local_data_file),
            unzip_dir = Path(config.unzip_dir)
        )

        return data_ingestion_config
    
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.base_model_preparation
        params = self.params

        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir = Path(config.root_dir),
            base_model_path = Path(config.base_model_path),
            updated_base_model_path = Path(config.updated_base_model_path),
            params_image_size = list(params.IMAGE_SIZE),
            params_learning_rate = float(params.LEARNING_RATE),
            params_include_top = bool(params.INCLUDE_TOP),
            params_weights = str(params.WEIGHTS),
            params_classes = int(params.CLASSES)
        )

        return prepare_base_model_config
    
    def get_prepare_callback_config(self) -> PrepareCallbackConfig:
        config = self.config

        create_directories([
            Path(config.prepare_callbacks.tensorboard_log_dir),
            Path(config.prepare_callbacks.checkpoint_dir)
        ])

        prepare_callback_config = PrepareCallbackConfig(
            root_dir = Path(config.artifacts_root),
            tensorboard_log_dir = Path(config.prepare_callbacks.tensorboard_log_dir),
            checkpoint_dir = Path(config.prepare_callbacks.checkpoint_dir)
        )

        return prepare_callback_config