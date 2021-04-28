import logging
import pickle

from flask import Flask
from blueprint import construct_blueprint
from utils_ext import Action, State, QLearner

# Change global variables as needed
LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.5
RANDOM_CHANCE = 0.1
MODEL_FILENAME = "src/data/q_learner.pkl"

# Set up logging format
fmt = logging.Formatter(
          fmt='%(asctime)s [%(levelname)s] %(module)s: %(message)s',
          datefmt='%Y-%m-%dT%H:%M:%S%z')

# Set up logging to stream
fh = logging.StreamHandler()

# Get the root logger
logger = logging.getLogger()

# Set level and add handler
logger.setLevel(logging.INFO)
fh.setFormatter(fmt)
logger.addHandler(fh)

# Define Flask application
app = Flask(__name__)

q_learner = QLearner(
    learning_rate=LEARNING_RATE,
    discount_rate=DISCOUNT_RATE,
    random_chance=RANDOM_CHANCE
)
# with open(MODEL_FILENAME, 'wb') as file:
#     q_learner = pickle.load(file)
app.register_blueprint(construct_blueprint(q_learner))

# Just a test endpoint
@app.route('/')
def index():
    return "This API is Alive"

@app.route('/all-endpoints')
def all_endpoints():
    return str([str(rule) for rule in app.url_map.iter_rules()])

# Run the flask app
if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
