from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
app.debug = True

api = Api(app)

class Root(Resource):
    def get(self):
        return { 'result': 'Hello, world!' }

api.add_resource(Root, '/')

if __name__ == '__main__':
    app.run()
