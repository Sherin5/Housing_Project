from housing.pipeline.pipeline import pipeline
from housing.config.configuration import Configuration
from housing.component.data_transformation import *

def main():
    try:
        #schema_file_path = r"/Users/sherinthomas/Downloads/Python/Housing_Project/config/schema.yaml"
        #file_path = r"/Users/sherinthomas/Downloads/Python/Housing_Project/housing/artifact/data_ingestion/2022-10-16-10-46-36/ingested_data/train/housing.csv"
        #df = DataTransformation.load_data(file_path = file_path, schema_file_path =schema_file_path)
        #print(df.dtypes)
        #print(df.columns)
        pipeline().run_pipeline()
        #pipeline.run_pipeline()
        #data_validation_config = Configuration().get_data_validation_config()
        #print(data_validation_config)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()