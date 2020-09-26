from flask_restful import Api, Resource


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}