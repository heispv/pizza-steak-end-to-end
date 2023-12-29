import os
import json
import yaml
import joblib
import base64
from box import ConfigBox
from box.exceptions import BoxValueError
from PizzaSteakClassifier import logger
from ensure import ensure_annotations
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml_file(path_to_yaml_file: Path) -> ConfigBox:
    """
    Read a YAML file and return its contents as a ConfigBox object.

    Args:
        path_to_yaml_file (Path): The path to the YAML file.

    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.

    Raises:
        ValueError: If the YAML file is empty.

    """
    try:
        with open(path_to_yaml_file, "r") as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
            logger.info(f"YAML file loaded successfully: {path_to_yaml_file}")
            return ConfigBox(yaml_dict)
    except BoxValueError:
        logger.info(f"YAML file is empty: {path_to_yaml_file}")
        raise ValueError(f"YAML file is empty: {path_to_yaml_file}")
    except Exception as e:
        logger.info(f"Error while loading YAML file: {path_to_yaml_file}")
        raise e
    
@ensure_annotations
def create_directories(dirs_path: list, verbose=True):
    """
    Create directories.

    Args:
        dirs_path (list): A list of directories to create.
        verbose (bool, optional): Whether to print the directories created. Defaults to True.

    """
    for dir_path in dirs_path:
        os.makedirs(dir_path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created: {dir_path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save a dictionary as a JSON file.

    Args:
        path (Path): The path to the JSON file.
        data (dict): The dictionary to save.

    """
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    logger.info(f"JSON file saved: {path}")

def decode_image(imgstr, filename):
    """
    Decode the base64 encoded image string and save it as a file.

    Args:
        imgstr (str): Base64 encoded image string.
        filename (str): Name of the file to save the decoded image.

    Returns:
        None
    """
    imgdata = base64.b64decode(imgstr)
    with open(filename, "wb") as f:
        f.write(imgdata)

def encode_image_into_base64(img_path):
    """
    Encode an image into base64 string.

    Args:
        img_path (str): Path to the image file.

    Returns:
        str: Base64 encoded image string.
    """
    with open(img_path, "rb") as f:
        imgstr = base64.b64encode(f.read())
    
    return imgstr.decode("utf-8")