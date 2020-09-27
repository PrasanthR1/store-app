from flask_restful import Resource
from json import loads
from flask import jsonify, request
from product.mongo import Mongo
from product.kafkaQueue import KafkaQueue
from product import app, api


class GetOrCreateProduct(Resource, Mongo):
    """
    This is a class for getting and creating products using mongodb
    :methods:
        get
        post
    """
    @staticmethod
    def get():
        """
        It is a GET method, which will get all the products from mongodb.
            :status: 200
            :rtype: list
            :except: Exception
            :return: All the products which is stored in db
        """
        output = Mongo.get_all_products()
        return loads(output)

    @staticmethod
    def post():
        """
        It is a POST method, which will post products to mongodb.
        :status: 200
        :rtype: dict
        :return: product which is posted to db
        """
        output = Mongo.post_product()
        return jsonify(output)


class GetOrUpdateProductById(Resource, Mongo):
    """
    This is a class for get or update or delete a product by its Product ID
    :methods:
        get(pid)
        put(pid)
        delete(pid)
    """
    @staticmethod
    def get(pid: int) -> dict:
        """
        It is a GET method, which requires a parameter Product ID
        :param pid: Product ID
        :rtype: dict
        :return: A product which is related to Product ID
        """
        output = Mongo.get_product_by_id(pid)
        return loads(output)

    @staticmethod
    def put(pid: int) -> dict:
        """
        It is a UPDATE method, which will update a product by Product ID
        :param pid: Product ID
        :rtype: dict
        :return: Product which is updated by Product ID
        """
        j = request.get_json()
        output = Mongo.update_product_by_id(pid, j)
        return loads(output)

    @staticmethod
    def delete(pid: int) -> str:
        """
        It is a DELETE method, which will delete a product by its Product ID
        :param pid: Product ID
        :rtype: str
        :return: Success Message
        """
        output = Mongo.delete_product_by_id(pid)
        return jsonify(output)


class WriteReadTopic(Resource, KafkaQueue):
    """
    This is a class for Reading and writing the queue messages from kafka to mongodb
    :method:
        post(topic)
    """
    @staticmethod
    def post(topic: str) -> list:
        """
        This is a POST method, which will publish Product ID,Product price to Queue
        and consume the Product ID,Product price and add/update the product price to
        mongodb by its Product ID
        :param topic: topic name where the messages are published
        :rtype: list
        :return: [{"200", "ok"}]
        """
        json = request.get_json()
        KafkaQueue.producer(topic, json)
        KafkaQueue.consumers()
        # print(json)
        return jsonify(200, "OK")


api.add_resource(GetOrCreateProduct, "/products", endpoint="products")
api.add_resource(GetOrUpdateProductById, "/product/<int:pid>", endpoint="product")
api.add_resource(WriteReadTopic, "/post/<string:topic>", endpoint="post")

# print(GetOrCreateProduct.get.__doc__)
# help(GetOrCreateProduct.get)

if __name__ == "__main__":
    app.run(debug=False)
