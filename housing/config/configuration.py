from housing.entity.config_entity import *
from housing.constants import *
from housing.util.util import read_yaml
from housing.exception import HousingException
from housing.constants import *
import os, sys
from housing.logger import logging

class Configuration:
    def __init__(self,config_file_path = CONFIG_FILE_PATH,current_time_stamp:str= CURRENT_TIME_STAMP):
        try:
            self.config_info = read_yaml(config_file_path)
            self.training_pipeline = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info= self.config_info[DATA_INGESTION_CONFIG_KEY]
            DATA_INGESTION_URL  = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            artifact_dir= self.training_pipeline.artifact_dir
            data_ingestion_artifact_dir= os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]

            )
            RAW_DATA_DIR = os.path.join(
                data_ingestion_artifact_dir, 
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )
            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_DIR_NAME_KEY]
            )
            INGESTED_TRAIN_DIR=os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            INGESTED_TEST_DIR= os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )
            data_ingestion_config = DataIngestionConfig(
                dataset_download_url =DATA_INGESTION_URL , 
                tgz_download_file=tgz_download_dir, 
                raw_data_dir=RAW_DATA_DIR, 
                ingested_train_dir=INGESTED_TRAIN_DIR, 
                ingested_test_dir=INGESTED_TEST_DIR
            )
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        pass

    def get_data_transformation_config(self)->DataTransformationConfig:
        pass

    def get_model_trainer_config(self)->ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self)->ModelPusherConfig:
        pass

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,training_pipeline_config[TRAINING_PIPELINE_NAME_KEY], training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir = artifact_dir)
            logging.info(f"Training pipeline config: {training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e,sys) from e





