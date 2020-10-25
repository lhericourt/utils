# Docker container
## Container livecycle 
- `docker container run --name NAME --network NETWORK --rm -d -p HOST_PORT:CONTAINER_PORT -e ENV_VARIABLE_NAME=ENV_VARIABLE_VALUE CONTAINER_IMAGE` : Donwload the image if not if cache, create a container and run it
  - -d :is to detach the process 
  - --rm : remove the container once it is exited
- `docker container exec -it CONTAINER_IMAGE COMMAND`: execute the command on a running container
  - -i : keep session open (interactive) 
  - -t : allocate a pseudo tty
- `docker container start CONTAINER`: start a container
- `docker container stop CONTAINER`: stop a container
- `docker container rm CONTAINER` : remove a container

## Instpect container
- `docker container ls`: list all active containers
- `docker container ls -a` : list all containers
- `docker container top CONTAINER` : list processes within the container
- `docker container inspect CONTAINER` : show the metadata
- `docker container stats` : give a streaming view of live performances of containers
***
# Docker Network
## Network lifecyle
- `docker network create NETWORK` : create a new virtual network
- `docker network connect CONTAINER_ID NETWORK_ID` : connect the container to the network
- `docker network disconnect CONTAINER_ID NETWORK_ID` : disconnect the container to the network

## Inspect network
- `docker network ls`: list all created networks
- `docker network inspect ` : show the metadata of the network and the containers attached to it

## Notes
- When creating a new network, the dns option is already set up also you can use directly the container names as host
- On the default network you need to use the option --link to enable the dns feature
***
# Docker Image
## Image lifecyle
- `docker pull IMAGE:TAG`: download the version of the image from dockerhub referenced by the TAG ; the TAG is optitonal it takes the lastest if not specified
- `docker image tag IMAGE:TAG NEW_IMAGE:NEW_TAG`: download the version of the image from dockerhub referenced by the TAG ; the TAG is optional
- `docker push IMAGE:TAG`: upload the version of the image to dockerhub
## Inspect image
- `docker image ls`: list all downloaded images
- `docker image history IMAGE`: show layers of changes made in image
