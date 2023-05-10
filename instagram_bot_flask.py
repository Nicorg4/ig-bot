from flask import *
from instagram_bot import *

app = Flask(__name__)

@app.route('/start_cycle', methods=['GET'])
def home_page():
    start_bot()
    return Response("{'a':'b'}", status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=7777)

