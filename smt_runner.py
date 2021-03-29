import sys
from kafka import KafkaConsumer, KafkaProducer
from json import loads
from pydoc import locate
from kafka.errors import KafkaError

import logging
import yaml

# read config
if len(sys.argv) > 1:
    # read from command line
    if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "-?":
        print("to use: python smt_runner.py <path to yaml config file>")
        sys.exit()
    else:
        configfile = sys.argv[1]
else:
    configfile = "/app/config.yaml"
with open(configfile, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.error(exc)

# set log level
logging.getLogger().setLevel(config.get("loglevel", "info").upper())


consumer = KafkaConsumer(
    config["consumer_topic"],
    bootstrap_servers=[config["consumer_server"]],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=config["group_id"],
)
logging.info(f"connected to consumer at {config['consumer_server']}")

# dynamically load the transformer
transformer_class = locate(config["classname"])
transformer = transformer_class(config["properties"])

producer = KafkaProducer(
    bootstrap_servers=[config["consumer_server"]]
)
logging.info(f"connected to producer at {config['consumer_server']}")

for message in consumer:
    logging.debug(message.value)
    try:
        transformed_message = transformer.transform(message.value)
        logging.info(transformed_message)

        # write to new topic if we need to
        if "producer_topic" in config and config["producer_topic"]!="":
            producer.send(config['producer_topic'], transformed_message)

    except Exception as e:
        logging.error("transform error")
        logging.error(e)
        if not config["error_handling"] == "ignore":
            raise ValueError("error in transform")
