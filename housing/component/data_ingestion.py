from housing.entity.config_entity import *
from housing.exception import HousingException
from housing.logger import logging
import os, sys
from housing.entity.artifact_entity import *
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


def testing(data_ingestion_config:DataIngestionConfig):
    return data_ingestion_config.dataset_download_url

class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'='*20 } Data Ingestion log started {'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def download_housing_data(self)-> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir, exist_ok=True)
            housing_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)
            logging.info(f"Downloading file from {download_url} into dir {tgz_file_path} ")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File downloaded completely into dir {tgz_file_path} ")
            return tgz_file_path
        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self, tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(tgz_file_path)

            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"Extracting tgz file {tgz_file_path} into {raw_data_dir } ")
            with tarfile.open(tgz_file_path) as housing_tgz_file_object:
                housing_tgz_file_object.extractall(path=raw_data_dir)
            logging.info(f"Extraction complete")
        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir  = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            housing_file_path = os.path.join(raw_data_dir, file_name)
            logging.info(f"Reading the CSV file {housing_file_path} ")
            housing_data_frame = pd.read_csv(housing_file_path)
            housing_data_frame["income_category"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0,1.5,3.0,4.5,6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            strat_train_set = None
            strat_test_set= None
            split = StratifiedShuffleSplit(n_splits=1,test_size=0.2, random_state=42 )
            for train_index, test_index in split.split(housing_data_frame, housing_data_frame["income_category"]):
                strat_train_set= housing_data_frame.loc[train_index].drop(["income_categort"], axis=1)
                strat_test_set= housing_data_frame.loc[test_index].drop(["income_categort"], axis=1)
            train_file_path= os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path =  os.path.join(self.data_ingestion_config.ingested_test_dir , file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting the train data into CSV file {train_file_path} ")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting the test data into CSV file {test_file_path} ")
                strat_test_set.to_csv(test_file_path, index=False)
            data_ingestion_artifact= DataIngestionArtifact(train_file_path=train_file_path, 
                                    test_file_path=test_file_path, 
                                    is_ingested=True, 
                                    message= "data ingestion completed")
            return data_ingestion_artifact

            

        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f" {'='*20} data ingestion log completed {'='*20} ")