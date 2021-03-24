# running in docker

The default image dynamically loads a class file and a config.yml file.
In case you want to build the image, a Dockerfile is provided in the repository.

When running in docker, the module will add /app to the PYTHONPATH. The config.yml and the python class file should be mapped there.

```
docker run --net=host -v $(pwd):/app smtdocker
```
