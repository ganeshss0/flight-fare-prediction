from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
def homePage():
    """
    Renders Home Page
    """
    return render_template('index.html')
