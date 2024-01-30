from PizzaSteakClassifier.config.configuration import ConfigurationManager
from PizzaSteakClassifier.components.prepare_base_model import PrepareBaseModel
from PizzaSteakClassifier import logger


STAGE_NAME = "Prepare Base Model"

class PrepareBaseModelPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.download_base_model()
        prepare_base_model.update_base_model()
    
    def run(self):
        try:
            logger.info(f"-------------Running stage: {STAGE_NAME}-------------")
            self.main()
            logger.info(f"-------------Completed stage: {STAGE_NAME}------------\nx==============================x")
        except Exception as e:
            logger.exception(f"Exception in stage: {STAGE_NAME}")
            raise e
        
if __name__ == "__main__":
        PrepareBaseModelPipeline().run()