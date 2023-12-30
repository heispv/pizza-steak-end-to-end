import os
import urllib.request as request
import zipfile
from pathlib import Path
from PizzaSteakClassifier import logger
from PizzaSteakClassifier.utils.common import get_size
from PizzaSteakClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_data(self):
        """
        Downloads the data from the specified source URL and saves it locally.

        If the local data file already exists, it logs a message indicating its size.
        If the local data file does not exist, it downloads the file and logs the download details.

        Returns:
            None
        """
        if not os.path.exists(self.config.local_data_file):
            file_name, headers = request.urlretrieve(
                url = self.config.source_url,
                filename = self.config.local_data_file
            )
            logger.info(f"Downloaded {file_name} of size {get_size(Path(self.config.local_data_file))}")
        else:
            logger.info(f"Data file {self.config.local_data_file} already exists with the size {get_size(Path(self.config.local_data_file))}")

    def unzip_data(self):
            """
            Unzips the data file to the specified directory.

            Args:
                self.config.local_data_file (str): The path to the local data file.
                self.config.unzip_dir (str): The directory where the data file will be extracted.

            Returns:
                None
            """
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(self.config.unzip_dir)
