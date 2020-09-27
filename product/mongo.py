from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import json_util
from config import Config
from product import app
import logging

conf = Config()
app.config["MONGO_URI"] = conf.mongourl
mongo = PyMongo(app)

logging.basicConfig(level=logging.ERROR, filename="product/logs/Mongo.log", filemode="w")


class Mongo:
    @staticmethod
    def get_all_products():
        try:
            product = mongo.db.products
            prods = product.find()
            # print(json_util.dumps(s))
            return json_util.dumps(prods, default=json_util.default)
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def post_product():
        try:
            product = mongo.db.products
            # r = request.get_json()
            # print(r)
            p_id = request.json["product_id"]
            p_description = request.json["product_description"]
            p_name = request.json["product_name"]
            prod = product.find_one({"product_id": p_id})
            if prod is not None:
                out = "product id already exists!"
            else:
                inserted_id = product.insert(
                    {
                        "product_id": p_id,
                        "product_description": p_description,
                        "product_name": p_name,
                    }
                )
                demo_products = product.find_one({"_id": inserted_id})
                out = {
                    "product_id": demo_products["product_id"],
                    "product_description": demo_products["product_description"],
                    "product_name": demo_products["product_name"],
                }
            return out
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def get_product_by_id(pid):
        try:
            product = mongo.db.products
            s = product.find_one({"product_id": pid})
            # print(s)
            if s:
                out = json_util.dumps(s, indent=1, default=json_util.default)
            else:
                out = f"No products found for this id{pid}!"
            return out
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def update_product_by_id(pid, j):
        try:
            product = mongo.db.products

            updated = product.find_one_and_update({"product_id": pid}, j)
            # print(updated["_id"])
            if updated is not None:
                demo_products = product.find_one({"_id": ObjectId(updated["_id"])})
                out = json_util.dumps(demo_products, indent=1, default=json_util.default)
            else:
                out = "No product to update!"
            return out
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def update_product_price(msgs):
        try:
            pid = msgs["product_id"]
            p_price = msgs["product_price"]
            product = mongo.db.products
            # print(p_price)
            product.update_one(
                {"product_id": pid}, {"$set": {"product_price": p_price}}
            )
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def delete_product_by_id(pid):
        try:
            product = mongo.db.products
            product_id = product.find_one_and_delete({"product_id": pid})
            # print(product_id)
            if product_id is not None:
                out = "product deleted!"
            else:
                out = f"No product found for this id:{pid}"
            return out
        except Exception as e:
            logging.error(str(e))
