"""
Module for running the flask app.
"""

import logging

from flask import Flask
from blueprint import construct_blueprint
from utils import QLearner
from utils_ext import Action, State

# Change global variables as needed
LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.5
RANDOM_CHANCE = 0.1
POSSIBLE_ACTIONS = [Action('message'), Action('no_message')]
INIT_STATE_PROPERTIES = [0, 0]
MODEL_FILENAME = "rl_flask/data/q_learner.pkl"

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

# Initialize QLearner
q_learner = QLearner(
    learning_rate=LEARNING_RATE,
    discount_rate=DISCOUNT_RATE,
    random_chance=RANDOM_CHANCE,
    possible_actions=POSSIBLE_ACTIONS
)

# Initialize state
state = State(INIT_STATE_PROPERTIES)

# with open(MODEL_FILENAME, 'wb') as file:
#     q_learner = pickle.load(file)

# Register blueprint using initialized q_learner and state
app.register_blueprint(construct_blueprint(q_learner, state))


@app.route('/')
def index():
    """Test endpoint."""
    return "This API is Alive"


@app.route('/all-endpoints')
def all_endpoints():
    """Lists all available endpoints."""
    return str([str(rule) for rule in app.url_map.iter_rules()])


# Run the flask app
if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
