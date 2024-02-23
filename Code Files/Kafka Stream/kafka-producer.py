import json
from confluent_kafka import Producer
import uuid

def read_ccloud_config(config_file):
    omitted_fields = set(['schema.registry.url', 'basic.auth.credentials.source', 'basic.auth.user.info'])
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                if parameter not in omitted_fields:
                    conf[parameter] = value.strip()
    return conf

def produce_messages(producer, topic, messages):
    for message in messages:
        # Check if "key" is present in the message, generate a unique key if not
        key_value = str(message.get("key", str(uuid.uuid4())))
        producer.produce(topic, key=key_value, value=json.dumps(message))
    producer.flush()

# Load JSON file
with open("D:/DBDA Project/Code Files/Kafka Stream/sv_to_json_47627147.json") as json_file:
    messages_from_json = json.load(json_file)

# Initialize Kafka producer
producer = Producer(read_ccloud_config("D:/DBDA Project/Code Files/Kafka Stream/client.properties"))

# Specify Kafka topic
kafka_topic = "new"

# Produce messages
produce_messages(producer, kafka_topic, messages_from_json)
