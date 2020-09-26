from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import json_util
from config import Config
from product import app

conf = Config()
app.config["MONGO_URI"] = conf.mongourl
mongo = PyMongo(app)


class Mongo:
    def get_all_prodcuts(self):
        product = mongo.db.products
        prods = product.find()
        # print(json_util.dumps(s))
        out = json_util.dumps(prods, default=json_util.default)
        return out

    def post_product(self):
        product = mongo.db.products
        r = request.get_json()
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

    def get_product_by_id(self, pid):
        product = mongo.db.products
        s = product.find_one({"product_id": pid})
        # print(s)
        if s:
            out = json_util.dumps(s, indent=1, default=json_util.default)
        else:
            out = f"No products found for this id{pid}!"
        return out

    def update_product_by_id(self, pid, j):
        product = mongo.db.products

        updated = product.find_one_and_update({"product_id": pid}, j)
        # print(updated["_id"])
        if updated is not None:
            demo_products = product.find_one({"_id": ObjectId(updated["_id"])})
            out = json_util.dumps(demo_products, indent=1, default=json_util.default)
        else:
            out = "No product to update!"
        return out

    def update_product_price(self, msgs):
        pid = msgs["product_id"]
        p_price = msgs["product_price"]
        product = mongo.db.products
        # print(p_price)
        product.update_one(
            {"product_id": pid}, {"$set": {"product_price": p_price}}
        )

    def delete_product_by_id(self,pid):
        product = mongo.db.products
        product_id = product.find_one_and_delete({"product_id": pid})
        # print(product_id)
        if product_id is not None:
            out = "product deleted!"
        else:
            out = f"No product found for this id:{pid}"
        return out