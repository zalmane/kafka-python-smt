# About

This program consumes from a Kafka topic, runs a python class to perform a transformation, and produces it to another kafka topic. It is meant as a simple alternative to creating SMTs in Java in Kafka connect, or using Streams/Ksql (which is more efficient since it avoids a consume/produce operation).
For convenience, a Dockerfile is provided which can be easily deployed in K8s or any other containerized env.

# SMT class spec

The SMT class spec is a simple python file with a single class that inherits from `kafkasmt.KafkaSmt`.
Here is an example of the most simple SMT:

```
from typing import Dict
from kafkasmt import KafkaSmt


class Myclass(KafkaSmt):

    def transformJson(self, message: Dict) -> Dict:
        return {"hello": message}

```

There are several method signatures that can be overriden:

```
    def __init__(self, config: Dict):
        pass
```

Process the raw message

```
    def transform(self, message: bytes) -> bytes:
        return json.dumps(self.transformJson(message.decode())).encode()
```

Process a json message

```
    def transformJson(self, message: Dict) -> Dict:
        return message
```

# Config file

The config file defines the following properties:

```
error_handling: ignore
consumer_server: localhost:9092
consumer_topic: connect-test
producer_topic: connect-test-out
producer_server: localhost:9092
group_id: smt_group1 # used to scale-out. Use the same group_id for multiple python-smt instances to parallel process
classname: mysmt.Myclass # name of the class to use. Will be searched in PYTHONPATH.
loglevel: debug
properties: # any custom properties, to be passed to the __init__ of the custom class
  myprop: 1
```

# Running in docker

The default image dynamically loads a class file and a config.yml file.
Use the Dockerfile provided in the repository to build the container.

When running in docker, the module will add /app to the PYTHONPATH. The config.yml and the python class file should be mapped there. These can be provided using a mapped volume or bundled into the container.

Build

```
docker build  --tag smtdocker .
```

Run

```
docker run --net=host -v $(pwd):/app smtdocker
```
