# Housing_Project

The below command is used to create the connection between docker and the application that I have created. $PORT is the port variable that we get from docker. Also note, the docker image name should always be in lowercase
```
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
```

To list all the docker images :
```
docker images
```

To run the image 
```
docker run -p 5000:5000 -e PORT=5000 <imageid>
```

To check running containers in docker
```
docker ps
```

To stop docker container
```
docker stop <container_id>
```

Why do we create Machine Learning Pipeline?
The pipeline will consist of the following:
1.  Data Ingestion: as this is the first step where we ingest the data into the model from multiple sources. We will also split the data into train, validation, and test data
2.  Data Validation: This includes schema validation. Data type and no. of columns in the file. The structure of the data, null check, imbalanced data
3.  Data transformation: featurr engineering
4.  Model traning: Model selection, hyperparameter tuning
5.  Model Evaluation: Test the model on the test data
6.  Push Model: Push the model to the CI/CD pipeline

What is an artifact?
Artifact is something that is not naturally present but becomes evident due to the research. So here all the outputs are defined as artifacts. The entity folder will consist of artifacts of all the steps: Data Ingestion artifact, Data validation artifact, data transformation artifact, model trainer artifact, model evaluation artifact, and Model pusher artifact.

Install the ipynbkernel to run jupyter notebook
```
pip install ipykernel
```




