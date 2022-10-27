import yaml
from housing.exception import HousingException
import os, sys
from housing.constants import *
import numpy as np
import dill
import pandas as pd

def read_yaml(file_path:str)->dict:
    """
    read the contents of the yaml file
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e

def save_numpy_array(file_path:str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e,sys) from e

def load_numpy_array(file_path: str)-> np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 

def save_object(file_path:str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 

def load_object(file_path:str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise HousingException(e, sys) from e 
        
def load_data(file_path: str, schema_file_path: str)-> pd.DataFrame:
    try:
        dataset_schema = read_yaml(schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        df = pd.read_csv(file_path)
        error_message = ""
        for cols in df.columns:
            if cols in list(schema.keys()):
                df[cols].astype(schema[cols])
            else:
                error_message = f"{error_message} \n Column {cols} is not in schema"

        if len(error_message) >0:
            raise Exception(error_message) 
        return df
    except Exception as e:
        raise HousingException(e, sys) from e






