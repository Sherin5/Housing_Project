
from housing.entity.model_factory import ModelFactory
from symbol import test
from housing.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from housing.entity.config_entity import ModelTrainerConfig
from housing.entity.artifact_entity import ModelTrainerArtifact
from housing.exception import HousingException
import os, sys
from housing.logger import logging
from housing.util.util import *

class HousingEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object) :
        
        self.preprocessing_object =preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)


class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact) :
        try:
            logging.info(f"{'>>'*30} Model trainer log started. {'<<'*30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e 

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info(f"loading transformed training dataset")
            trasformed_train_file_path =  self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array(file_path=trasformed_train_file_path)

            logging.info(f"loading transformed test dataset")
            transfomed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array(file_path=transfomed_test_file_path)

            logging.info(f"splitting training and testing data into input and target feature")
            x_train, y_train, x_test, y_test = train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1]

            logging.info(f"extracting model config path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing modelfactory class using the above model config path {model_config_file_path} ")
            model_factory = ModelFactory(model_config_path= model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected Accuracy : {base_accuracy}")

            logging.info(f"initiating model selection operation")
            best_model = 

        except Exception as e:
            raise HousingException(e, sys) from e
