import yaml
from housing.exception import HousingException
import os, sys
from housing.constants import *

def read_yaml(file_path:str)->dict:
    """
    read the contents of the yaml file
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e

read_yaml("/Users/sherinthomas/Downloads/Python/Housing_Project/config/config.yaml")




