from flask import Flask

app = Flask(__name__)

@app.route("/api")
def index_api():
    return {"message": "hello"}