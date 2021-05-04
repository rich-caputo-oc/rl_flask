"""
Module for defining specific RL problem and creating endpoints.
"""

import json
import pickle
from flask import Blueprint, request
from flask_cors import cross_origin

from utils import QLearner
from utils_ext import State, get_action_from_args, get_state_from_args


def construct_blueprint(q_learner: QLearner, state: State) -> Blueprint:
    """
    Constructs Blueprint responsible for all RL endpoints.
    Args:
        q_learner: QLearner which updates as endpoints are called.
        state: State which updates as endpoints are called.
    Returns:
        Blueprint
    """
    main = Blueprint('main', __name__)

    @cross_origin()
    @main.route('/dump')
    def dump(directory: str = 'rl_flask/data'):
        """Dumps model to passed directory."""
        filename = directory + '/' + request.args.get('file', 'q_learner.pkl')
        with open(filename, 'wb') as file:
            pickle.dump(q_learner, file)
        return f"Model dumped to {filename}"

    @cross_origin()
    @main.route('/get_action')
    def get_action():
        """Given current state / passed state, gets RL agent's action."""
        if 'state' in request.args:
            action = q_learner.get_action(get_state_from_args(request.args))
            return str(action)
        action = q_learner.get_action(state)
        return str(action)

    @cross_origin()
    @main.route('/get_current_state')
    def get_current_state():
        """Gets current state of the environment."""
        return str(state)

    @cross_origin()
    @main.route('/print_q_table')
    def print_q_table():
        """Prints Q table."""
        table = {}
        for state_, dict_ in q_learner.table.items():
            action_space = {}
            for action_, reward_ in dict_.items():
                action_space[str(action_)] = reward_
            table[str(state_)] = action_space
        return json.dumps(table, indent=4, sort_keys=True)

    @cross_origin()
    @main.route('/reset_state')
    def reset_state():
        """Resets current state."""
        state.reset()
        return f"StateBase reset to {state}"

    @cross_origin()
    @main.route('/update')
    def update():
        """
        Updates RL model using current state, action taken,
        and the reward from the state action pair.
        """
        input_state = request.args.get('state', None)
        reward = float(request.args.get('reward', 0))
        terminal = bool(request.args.get('terminal', False))
        if input_state is not None:
            action = q_learner.get_action(get_state_from_args(input_state))
        else:
            action = get_action_from_args(request.args)
        q_learner.update(state=state, action=action, reward=reward, terminal=terminal)
        return str(state)

    return main
