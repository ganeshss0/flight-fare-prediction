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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)