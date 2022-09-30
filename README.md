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