import os
from Classifier.constants import *
from Classifier.utils.common import read_yaml, create_directories
# from Classifier.entity.config_entity import (DataIngestionConfig,
#                                                 PrepareBaseModelConfig,
#                                                 TrainingConfig,
#                                                 EvaluationConfig)


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config["artifact_root"]])
    
    def get_data_extraction_config(self):
        config = self.config["data_extraction"]

        data_extraction_config = {"user":os.getenv("DB_USER"),
            "password":os.getenv("DB_PASSWORD"),
            "host":os.getenv("DB_HOST"),
            "database":config["database"],
            "table":config["table"] }

        return data_extraction_config
    

    def get_data_training_config(self):
        self.config["training"]["root_dir"]=Path(self.config["training"]["root_dir"])
        self.config["training"]["trained_model_path"]=Path(self.config["training"]["trained_model_path"])
        data_training_config = {"params":self.params,
                              "training":self.config["training"]}

        return data_training_config

    # def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
    #     config = self.config.prepare_base_model
        
    #     create_directories([config.root_dir])

    #     prepare_base_model_config = PrepareBaseModelConfig(
    #         root_dir=Path(config.root_dir),
    #         base_model_path=Path(config.base_model_path),
    #         updated_base_model_path=Path(config.updated_base_model_path),
    #         params_image_size=self.params.IMAGE_SIZE,
    #         params_learning_rate=self.params.LEARNING_RATE,
    #         params_include_top=self.params.INCLUDE_TOP,
    #         params_weights=self.params.WEIGHTS,
    #         params_classes=self.params.CLASSES
    #     )

    #     return prepare_base_model_config
    


    # def get_training_config(self) -> TrainingConfig:
    #     training = self.config.training
    #     prepare_base_model = self.config.prepare_base_model
    #     params = self.params
    #     training_data = os.path.join(self.config.data_ingestion.unzip_dir, "Chest-CT-Scan-data")
    #     create_directories([
    #         Path(training.root_dir)
    #     ])

    #     training_config = TrainingConfig(
    #         root_dir=Path(training.root_dir),
    #         trained_model_path=Path(training.trained_model_path),
    #         updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
    #         training_data=Path(training_data),
    #         params_epochs=params.EPOCHS,
    #         params_batch_size=params.BATCH_SIZE,
    #         params_is_augmentation=params.AUGMENTATION,
    #         params_image_size=params.IMAGE_SIZE
    #     )

    #     return training_config
    



    # def get_evaluation_config(self) -> EvaluationConfig:
    #     eval_config = EvaluationConfig(
    #         path_of_model="artifacts/training/model.h5",
    #         training_data="artifacts/data_ingestion/Chest-CT-Scan-data",
    #         mlflow_uri="https://dagshub.com/entbappy/chest-Disease-Classification-MLflow-DVC.mlflow",
    #         all_params=self.params,
    #         params_image_size=self.params.IMAGE_SIZE,
    #         params_batch_size=self.params.BATCH_SIZE
    #     )
    #     return eval_config
