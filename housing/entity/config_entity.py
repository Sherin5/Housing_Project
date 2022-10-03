from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", 
["dataset_download_url", "tgz_download_file", "raw_data_dir", "ingested_train_dir", "ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["add_bedroom_per_room",
"transformed_train_dir", "transformed_test_dir", "preprocessed_file_path"]) ## Preprocesses file path is the path to the pickle object

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_file_path", "base_accuracy"])

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path", "time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])




