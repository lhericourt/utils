# Docker container
## Container livecycle 
- `docker container run --name NAME --network NETWORK --rm -d -p HOST_PORT:CONTAINER_PORT -e ENV_VARIABLE_NAME=ENV_VARIABLE_VALUE -v VOLUME_NAME:VOLUME_DESTINATION CONTAINER_IMAGE` : Donwload the image if not if cache, create a container and run it
  - -d :is to detach the process 
  - --rm : remove the container once it is exited
  - -v : to mount a volume (e.g. db data) or a directory, the difference is if the volume_name is a path then it is a bind mount (a link to the directory)
- `docker container exec -it CONTAINER_IMAGE COMMAND`: execute the command on a running container
  - -i : keep session open (interactive) 
  - -t : allocate a pseudo tty
- `docker container start CONTAINER`: start a container
- `docker container stop CONTAINER`: stop a container
- `docker container rm CONTAINER` : remove a container
- `docker container run --name NAME -d --health-cmd="COMAND" CONTAINER_IMAGE` : run the container and add a health check, the command has to return 0 or 1 (0 for OK 1 for KO)

## Instpect container
- `docker container ls`: list all active containers
- `docker container ls -a` : list all containers
- `docker container top CONTAINER` : list processes within the container
- `docker container inspect CONTAINER` : show the metadata
- `docker container stats` : give a streaming view of live performances of containers
- `docker container logs CONTAINER` : show logs container
***
# Docker Network
## Network lifecyle
- `docker network create NETWORK --driver` : create a new virtual network
  - driver = overlay for swarm set up
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
- `docker pull IMAGE[:TAG]`: download the version of the image from dockerhub referenced by the TAG ; the TAG is optitonal it takes the lastest if not specified
- `docker image tag IMAGE[:TAG] NEW_IMAGE[:NEW_TAG]`: download the version of the image from dockerhub referenced by the TAG ; the TAG is optional
- `docker push IMAGE[:TAG]`: upload the version of the image to dockerhub
- `docker image build -t IMAGE:TAG DIRECTORY`: build the image from a docker file

## Inspect image
- `docker image ls`: list all downloaded images
- `docker image history IMAGE`: show layers of changes made in image

## Dokerfile file
It is the file taht contains all instructions to build an image

Main keywords : 
- `FROM`: image to build from
- `EXPOSE`: port that should be expose
- `RUN`: command to run ; we can use the symbol '&&' to chain several commands ; with this symbol the previous commands have to be sucessful in order the next one to be run
- `WORKDIR`: equivalent to a cd within the container
- `COPY`: copy a file from the hst to the container
***
# Docker Volume
## Volume lifecyle

## Inspect volume
- `docker volume ls`: list all volumes
- `docker volume inspect VOLUME`: show the metadata of the volume
***
# Docker compose
## Commands
A lot of commands available in docker are also available for docker-compose (-d, logs...)

Docker compose is use for development only
- `docker-compose [-f BASE_FILE] [-f OVERRIDE_FILE] up`: set volumes / networks and start all containers
  -  By default it takes the file named docker-compose.yml, but we can specify an override_file that contains more commands. It is useful when we have different environment, we can do one override file by environment (dev, ci, prod)
- `docker-compose down`: stop all containers and remove containers / networks
- `docker-compose build`: rebuild an existing image
- `docker-compose -f BASE_FILE -f OVERRIDE_FILE config`: combines the two files, and does the sames as the up command
## docker-compose.yml file
main keywords : 
- `image`: name of the image
- `build + context + dockerfile`: path to the dockerfile to build the image 
- `ports`: list of ports
- `environment`: keys/values of environment variables
- `volumes`: list of volumes to mound
- `command`: command to execute

Example : 
```
version: '3.1'

services:
  proxy:
    build:
      context: .
      dockerfile: nginx.Dockerfile
    image: nginx-custom
    ports:
      - '80:80'
  mypostgres:
    image: postgres
    environment:
      POSTGRES_DB: drupal
      POSTGRES_USER: user1
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - my-db:/var/lib/postgresql/data 
```

***
# Swarm
Swarm is the built-in orchestration tool of docker

Make sure everything is running, if not it restarts containers not running

Useful for production if we want to do updates of the environment without shutting down the service 

## Commands
- `docker swarm init`: activate swarm functionality, et deploy a node manager
- `docker swarm join-token ROLE`: get the command with the token to add a node 
  - ROLE can take the value worker or manager 
- `docker swarm join --token TOKEN`: add a node to a swarm 
- `docker node ls`: show info about nodes managed by swarm 
- `docker node update --role ROLE Node`: update a node to a worker role or a manager role
- `docker service COMMAND`: replace the docker run command in a swarm 
- `docker service ps IMAGE`: show infos of the image managed by swarm 
- `docker service create --replicas N --secret SECRET_NAME --name SERVICE_NAME IMAGE_NAME`: create a service from the image running on N replicas
  - secret : secret that the service can see, check next section about secrets
- `docker service update [--replicas N] [--image IMAGE NAME] [--env-add ENV_NAME=ENV_VALUE] [--publish-rm HOST_PORT] [--publish-add HOST_PORT:CONTAINER_PORT] SERVICE_NAME`: update the number of replicas for the specified service

## Secret Management

Swarm can manage secret securely (passwords, certificates, keys...); it is saved in its database (Raft DB)
Once in the db the only things that can have access to the uncrypted secrets are containers and services we assign then to
- `docker secret create SECRET_NAME FILE_PATH` : create a new secret
- `echo 'SECRET_VALUE' | docker secret create SECRET_NAME -` : same as previous command line

Note: You can use secrets in a docker compose file, but it works only when secrets are store in files ; it is not secure but it is a good way to have development environment looking the same as production environment  

***
# Stack
A stack is a list of swarm services (and volumes/networks) ; a stack can use only one swarm it means all the services will be managed by the same swarm. 
- `docker stack deploy -c COMPOSE_FILE STACK_NAME`: deploy or update an existing stack 
- `docker stack services STACK_NAME`: Show all the tasks of the stack 

Example : 
```
version: '3.1'

services:

  drupal:
    image: drupal:8.8.2
    ports:
      - "8080:80"
    volumes:
      - drupal-modules:/var/www/html/modules
      - drupal-profiles:/var/www/html/profiles
      - drupal-sites:/var/www/html/sites
      - drupal-themes:/var/www/html/themes
 
  postgres:
    image: postgres:12.1
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/psql-pw
    secrets:
      - psql-pw
    volumes:
      - drupal-data:/var/lib/postgresql/data

volumes:
  drupal-data:
  drupal-modules:
  drupal-profiles:
  drupal-sites:
  drupal-themes:

secrets:
  psql-pw:
    external: true
```
sdcdsf




