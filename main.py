from PizzaSteakClassifier import logger
from PizzaSteakClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline



STAGE_NAME = "Data Ingestion"
try:
    logger.info(f"-------------Running stage: {STAGE_NAME}-------------")
    pipeline = DataIngestionPipeline()
    pipeline.main()
    logger.info(f"-------------Completed stage: {STAGE_NAME}------------\nx==============================x\n")
except Exception as e:
    logger.exception(f"Exception in stage: {STAGE_NAME}")
    raise e