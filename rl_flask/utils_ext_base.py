"""
Module for templating user code to be used in utils_ext.py.
"""

from utils import Action, StateBase


class State(StateBase):
    """Class for states."""

    def next(self, action: Action = None, **kwargs):
        """
        Required method for getting next state, possibly given an action.
        Should only update the attributes of the class.
        """
        # YOUR CODE HERE
        return self

    def reset(self):
        """Resets state to original state."""
        # YOUR CODE HERE
        return self


def get_state_from_args(request_args: dict) -> State:
    """Define how to map request arguments to a State."""
    # YOUR CODE HERE
    return State()


def get_action_from_args(request_args: dict) -> Action:
    """Define how to map request arguments to an Action."""
    # YOUR CODE HERE
    return Action()
