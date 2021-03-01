import flask
from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "Very"


app.run()
