from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import compareOtherMajors

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route("/api/process", methods=['POST'])
@cross_origin()
def process_data():
    data = request.json
    selected_degrees = data.get('selectedDegrees', [])
    
    # compareOtherMajors.current_major = selected_degrees
    result = compareOtherMajors.compare(selected_degrees)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
