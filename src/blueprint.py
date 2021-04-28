"""
Module for defining specific RL problem
"""
import json
import pickle
from flask import Blueprint, request
from flask_cors import cross_origin

from utils_ext import State, QLearner, get_action_from_args, get_state_from_args


def construct_blueprint(q_learner: QLearner, state: State = State()) -> Blueprint:
    main = Blueprint('main', __name__)

    @main.route('/get_action')
    @cross_origin()
    def get_action():
        if 'state' in request.args:
            action = q_learner.get_action(get_state_from_args(request.args))
            return str(action)
        action = q_learner.get_action(state)
        return str(action)

    @main.route('/get_current_state')
    @cross_origin()
    def get_current_state():
        return str(state)

    @main.route('/update')
    @cross_origin()
    def update():
        input_state = request.args.get('state', None)
        if input_state is not None:
            action = q_learner.get_action(get_state_from_args(input_state))
            return str(action)
        action = get_action_from_args(request.args)
        reward = float(request.args.get('reward', 0))
        q_learner.update(state=state, action=action, reward=reward)
        return str(state)

    @main.route('/dump')
    @cross_origin()
    def dump(directory: str = 'src/data'):
        filename = directory + '/' + request.args.get('file', 'q_learner.pkl')
        with open(filename, 'wb') as file:
            pickle.dump(q_learner, file)
        return f"Model dumped to {filename}"

    @main.route('/print_q_table')
    @cross_origin()
    def print_q_table():
        table = {}
        for st, dict1 in q_learner.table.items():
            action_space = {}
            for ac, rwd in dict1.items():
                action_space[str(ac)] = rwd
            table[str(st)] = action_space
        return json.dumps(table, indent=4, sort_keys=True)

    @main.route('/reset_state')
    @cross_origin()
    def reset_state():
        state.reset()
        return f"State reset to {state}"

    return main
