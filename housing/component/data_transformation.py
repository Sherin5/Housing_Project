from socketserver import DatagramRequestHandler
from tkinter import E
from turtle import st
from housing.constants import *
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataTransformationConfig,  DataIngestionConfig, DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
import os, sys
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from housing.util.util import read_yaml, save_object, save_numpy_array, load_numpy_array, load_object, load_data

class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True, total_room_ix=3,population_ix=5,households_ix=6, total_bedrooms_ix=4, columns=None) :
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix =  self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)
            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_room_ix = total_room_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:,self.total_room_ix] / \
                                 X[:, self.households_ix]

            population_per_household = X[:, self.population_ix]/ \
                                        X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_room_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room
                ]
            else:
                generated_feature = np.c_[
                    X,room_per_household, population_per_household
                ]
            return generated_feature
        except Exception as e:
            raise HousingException(e,sys) from e

class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact):
        try :
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    @staticmethod
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

    def get_data_transformer(self)->ColumnTransformer:
        try:
            schema_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml(file_path=schema_path)
            numerical_column= dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_column = dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('feature_generator', FeatureGenerator(
                    add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                    columns=numerical_column
                    )),
                ('scaler', StandardScaler())
            ])

            cat_pipeline = Pipeline(
                steps=[
                    ('impute', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            preprocessing = ColumnTransformer([      
                ('num_pipeline',num_pipeline,numerical_column  ),
                ('cat_pipeline', cat_pipeline,categorical_column )
            ])
            return preprocessing
        except Exception as e:
            raise HousingException(e,sys) from e 

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            preprocessing_obj = self.get_data_transformer()
            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)
            schema = read_yaml(file_path=schema_file_path)
            target_column_name = schema[TARGET_COLUMN_KEY]
            input_feature_train = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train = train_df[target_column_name]

            input_feature_test = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test = test_df[target_column_name]            
            inp_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train)
            inp_feature_test_arr= preprocessing_obj.transform(input_feature_test)

            train_arr = np.c_[inp_feature_train_arr, np.array(target_feature_train)]
            test_arr = np.c_[inp_feature_test_arr, np.array(target_feature_test)]
            tranformed_train_dir = self.data_transformation_config.transformed_train_dir
            tranformed_test_dir = self.data_transformation_config.transformed_test_dir
            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")
            tranformed_train_file_path = os.path.join(tranformed_train_dir, train_file_name)
            tranformed_test_file_path = os.path.join(tranformed_test_dir,test_file_name )

            save_numpy_array(file_path=tranformed_train_file_path, array=train_arr)
            save_numpy_array(file_path=tranformed_test_file_path, array=test_arr)
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_file_path
            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)
            data_tranformation_artifact = DataTransformationArtifact(is_transformed=True, 
                                                                    message="Data Transformation Successful",
                                                                    transformed_train_file_path=tranformed_train_file_path,
                                                                    transformed_test_file_path=tranformed_test_file_path,
                                                                    preprocessed_object_file_path=preprocessing_obj_file_path)
            logging.info(f"Data Transformation Artifact : {data_tranformation_artifact}")
            return data_tranformation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e



