# Task 3
### Build
```commandline
docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)
```
### Run
```commandline
docker-compose up
```

### Notes
to run container's terminal via docker-compose
```commandline
docker-compose run {service_name} sh
 ```



compose commands:  
- depends_on: it does not wait for another service to finish, it only waits until the other services starts. see: depends_on  
- health_check: it does not start the service until the command returns success. see: healthcheck  
- create a shell script to order of initialisation of your containers/services. see: startup order  