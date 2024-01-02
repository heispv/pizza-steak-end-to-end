from PizzaSteakClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from PizzaSteakClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelPipeline


if __name__ == "__main__":
    DataIngestionPipeline().run()
    PrepareBaseModelPipeline().run()