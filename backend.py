from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import compareOtherMajors
from flask_restx import Api, Resource, fields
import jwt

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, Flask!"

api = Api(app)

# Define the model for a single array of strings
model = api.model('Model', {
    'selectedDegrees': fields.List(fields.String, required=True, description='List of selected degree names')
})

@app.route("/api/process", methods=['POST'])
class ProcessData(Resource):
    @api.expect(model)
    def post(self):
        data = api.payload
        selected_degrees = data.get('selectedDegrees', [])
        
        # Process the data here
        result = compareOtherMajors.compare(selected_degrees)
        
        return result