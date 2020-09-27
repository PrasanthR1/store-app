from json import dumps, loads
from kafka import KafkaClient, KafkaProducer, KafkaConsumer
from product.mongo import Mongo

kafka_client = KafkaClient(hosts="localhost:9092")


class KafkaQueue(Mongo):
    @staticmethod
    def producer(topic, json):
        # print(json)
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda m: dumps(m).encode("ascii"),
        )
        producer.send(topic, json)

    @staticmethod
    def consumers():
        consumer = KafkaConsumer(
            "product",
            group_id="my-group",
            bootstrap_servers=["localhost:9092"],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=1000,
            value_deserializer=lambda m: loads(m.decode("ascii")),
        )
        for msg in consumer:
            msgs = msg.value
            # print(msgs)
            Mongo.update_product_price(msgs)
