from flask import Flask, request, jsonify
from flask_cors import CORS
import compareOtherMajors

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route("/api/process", methods=['POST'])
def process_data():
    data = request.json
    selected_degrees = data.get('selectedDegrees', [])

    result = compareOtherMajors.compare(selected_degrees)

    return jsonify({
        "result": result
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
