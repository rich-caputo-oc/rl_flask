"""
Module for utilities.
"""

from utils import Action, StateBase


class State(StateBase):
    """Class for states."""

    def next(self, action: Action = Action()):
        """
        Required method for getting next state, possibly given an action.
        Should only update the attributes of the class.
        """
        # YOUR CODE HERE
        prop = action.properties
        if prop == 'message':
            self.properties[1] += 1
        self.properties[0] += 1
        return self

    def reset(self):
        """Resets state to original state."""
        # YOUR CODE HERE
        self.properties = [0, 0]
        return self


def get_state_from_args(request_args: dict) -> State:
    """Define how to map request arguments to a State."""
    # YOUR CODE HERE
    state = request_args.get('state', '0,0')
    state = [int(x) for x in state.split(',')]
    return State(state)


def get_action_from_args(request_args: dict) -> Action:
    """Define how to map request arguments to an Action."""
    # YOUR CODE HERE
    return Action(request_args.get('action', 'no_message'))
