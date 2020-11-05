# task_1
ML engineering tasks

Build image:  
```
docker build -t balbes_check --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
```
Run container  
```
docker run -v $(pwd)/volume:/home/balbes/task_1 balbes_check
```
