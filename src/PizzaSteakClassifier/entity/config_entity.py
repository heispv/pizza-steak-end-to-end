from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    data_dir: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int
    params_validation_split: float

@dataclass(frozen=True)
class PrepareCallbackConfig:
    root_dir: Path
    tensorboard_log_dir: Path
    checkpoint_dir: Path

@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    update_base_model_path: Path
    training_data: Path
    result_image_path: Path
    evaluation_pictures: Path
    params_epoch: int
    params_batch_size: int
    params_image_size: list
    params_validation_split: float