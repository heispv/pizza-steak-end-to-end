from PizzaSteakClassifier import logger
from PizzaSteakClassifier.config.configuration import ConfigurationManager
from PizzaSteakClassifier.components.prepare_callbacks import PrepareCallback
from PizzaSteakClassifier.components.model_training import Training


STAGE_NAME = "Model Training Pipeline"


class ModelTrainigPipeline:
    def __init__(self):
        pass

    def main(self):
            config=ConfigurationManager()
            prepare_callback_config = config.get_prepare_callback_config()
            prepare_callbacks = PrepareCallback(config=prepare_callback_config)
            callback_list = prepare_callbacks.get_tb_ckpt_callbacks()
            
            training_config = config.get_training_config()
            training = Training(config=training_config)
            training.get_base_model()
            training.data_preparation()
            training.train(callback_list=callback_list)
            training.plot_and_save_history()
            training.plot_validation_images_with_predictions()


    def run(self):
        try:
            logger.info(f"-------------Running stage: {STAGE_NAME}-------------")
            self.main()
            logger.info(f"-------------Completed stage: {STAGE_NAME}------------\nx==============================x")
        except Exception as e:
            logger.exception(f"Exception in stage: {STAGE_NAME}")
            raise e

if __name__ == "__main__":
        ModelTrainigPipeline().run()