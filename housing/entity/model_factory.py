from housing.exception import HousingException
import os, sys
import numpy as np
import yaml
from collections import namedtuple
from typing import List
from housing.logger import logging

GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

class ModelFactory:
    def __init__(self, model_config_path: str = None) :
        try:
            self.config : dict = ModelFactory.read_params(model_config_path)
            self.grid_search_cv_module : str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name : str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data: dict = self.config[GRID_SEARCH_KEY][PARAM_KEY]
            self.model_initialization_config: dict =  dict(self.config[MODEL_SELECTION_KEY])
            self.initialized_model_list = None
            self.grid_search_best_model = None
        except Exception as e:
            raise HousingException(e,sys) from e

    @staticmethod
    def read_params(config_path: str)-> dict:
        try:
            with open(config_path) as yaml_file:
                config:dict = yaml.safe_load(yaml_file)
                return config
        except Exception as e:
            raise HousingException(e,sys) from e