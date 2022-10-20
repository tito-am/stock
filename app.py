from flask import Flask
import git
from src.business_logic.process_query import create_business_logic
from src.business_logic.process_query import create_business_logic_baseline
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/caramelo/Downloads/stock-ftam-01df728fdebc-labonne.json"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return f'Hello fellow humans and zombiens, you should use a better route:!\nEX: get_stock_val/<ticker>\n'


@app.route('/get_stock_val/dummy/<ticker>', methods=['GET'])
def get_stock_value(ticker):
    bl = create_business_logic()
    prediction = bl.do_predictions_for(ticker)

    return f'Value of {ticker} for tomorrow : {prediction} (Linear Regression)\n'

@app.route('/get_stock_val/sma30/<ticker>', methods=['GET'])
def get_stock_value_baseline(ticker):
    bli = create_business_logic_baseline()
    prediction = bli.do_predictions_for(ticker)

    return f'Value of {ticker} for tomorrow : {prediction} (moving average 30 days)\n'

@app.route('/getversion/')
def getversion():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    return f'{sha}\n'


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
