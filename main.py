from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.debug = True

api = Api(app)

class Root(Resource):
    def post(self):
        args = request.get_json(force = True)
        return { 'respText': args['text'] }

api.add_resource(Root, '/')

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
