from flask_restful import Resource
from json import loads
from flask import jsonify, request
from product.helloword import HelloWorld
from product.mongo import Mongo
from product import app, api
from product.kafkaQueue import KafkaQueue


class GetOrCreateProduct(Resource):
    def get(self):
        output = Mongo.get_all_prodcuts(self)
        return loads(output)

    def post(self):
        output = Mongo.post_product(self)
        return jsonify(output)


class GetOrUpdateProductById(Resource):
    def get(self, pid):
        output = Mongo.get_product_by_id(self, pid)
        return loads(output)

    def put(self, pid):
        j = request.get_json()
        output = Mongo.update_product_by_id(self,pid,j)
        return loads(output)

    def delete(self, pid):
        output = Mongo.delete_product_by_id(self,pid)
        return jsonify(output)


class ReadWriteTopic(Resource):
    def post(self, topic):
        json = request.get_json()
        KafkaQueue.producer(self,topic,json)
        KafkaQueue.consumers(self)
        # print(json)
        return jsonify(200, "OK")


api.add_resource(HelloWorld, "/")
api.add_resource(GetOrCreateProduct, "/products", endpoint="products")
api.add_resource(GetOrUpdateProductById, "/product/<int:pid>", endpoint="product")
api.add_resource(ReadWriteTopic, "/post/<string:topic>", endpoint="post")


if __name__ == "__main__":
    app.run(debug=False)
