from PizzaSteakClassifier.config.configuration import ConfigurationManager
from PizzaSteakClassifier.components.data_ingestion import DataIngestion
from PizzaSteakClassifier import logger


STAGE_NAME = "Data Ingestion"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.unzip_data()
    
    def run(self):
        try:
            logger.info(f"-------------Running stage: {STAGE_NAME}-------------")
            self.main()
            logger.info(f"-------------Completed stage: {STAGE_NAME}------------\nx==============================x")
        except Exception as e:
            logger.exception(f"Exception in stage: {STAGE_NAME}")
            raise e
    
if __name__ == "__main__":
        DataIngestionPipeline().run()