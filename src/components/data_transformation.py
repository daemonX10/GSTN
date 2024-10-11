from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder # Ordinal Encoding for Categorical Variables convert them into Numerical Variables
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import os , sys
from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from src.utils.save import save_object

## Data Transformation Config   

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    
## Data Transformation Class

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_tranformation_object(self):
        try:
            logging.info('Data Transformation initiated')
            
            # Define which columns should be ordinal-encoded and which should be scaled
            
            categorical_cols = ['cut','color','clarity']
            numerical_cols = ['carat','depth','table']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair','Good','Very Good','Premium','Ideal']
            color_categories = ['D','E','F','G','H','I','J']
            clarity_categories= ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            
            logging.info('Pipeline Initiated')
            
            ## Numerical Pipeline
            pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ('pipeline',pipeline,numerical_cols)
            ])
            
            logging.info("Pipe completed")
            return preprocessor
        
        except Exception as e:
            logging.error('Error occured while Data Transformation')
            logging.error(str(e))
            raise CustomException('Error occured while Data Transformation')
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info('Read train and test data completed')
            logging.info(f'Train DataFrame Head: {train_df.head().to_string()}')
            logging.info(f'Test DataFrame Head: {test_df.head().to_string()}')
            
            logging.info('Obtaining Data Transformation/Preprocessing Object')
            
# The line `preprocessing_obj = self.get_data_tranformation_object()` is calling the
# `get_data_tranformation_object()` method of the `DataTransforation` class to obtain the data
# transformation/preprocessing object. This method sets up a pipeline for transforming the data by
# defining separate pipelines for numerical and categorical columns, including steps such as
# imputation and scaling for numerical columns, and ordinal encoding for categorical columns. The
# `ColumnTransformer` combines these pipelines into a single preprocessing object that can be used to
# transform the data.
            target_column_name = 'target'
            drop_columns = ['ID']
            
            input_features_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_features_train_df = train_df[target_column_name]
            
            input_features_test_df = test_df.drop(columns=drop_columns,axis=1)
            target_features_test_df = test_df[target_column_name]
            
            logging.info('Applying Data Transformation on Train and Test Data')
            
            ## Appling the transformation and creating the pickle for scaler
            
            preprocessing_obj = self.get_data_tranformation_object()
            
            input_features_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            
            input_features_test_arr = preprocessing_obj.transform(input_features_test_df)
            
            logging.info("Applying preprocessing object on train and test data completed")
            
            train_arr = np.c_[input_features_train_arr,np.array(target_features_train_df)]
            test_arr = np.c_[input_features_test_arr,np.array(target_features_test_df)]
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            
            logging.info('Processing Pickle in created and saved')
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            logging.error('Error occured while Data Transformation')
            logging.error(str(e))
            raise CustomException('Error occured while Data Transformation')