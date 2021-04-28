"""
Module for utilities.
"""
from typing import Any

from utils import Action, State, QLearner


class State(State):
    """Base class for states."""

    def __init__(self, properties: Any = [0, 0], terminal: bool = False):
        """
        Initialize state with a list of properties and
        bool describing whether or not state is terminal.
        """
        super().__init__(properties, terminal)

    def next(self, action: Action = None):
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


class QLearner(QLearner):
    """Class for Q Learning agent."""

    def __init__(
        self,
        learning_rate: float,
        discount_rate: float,
        random_chance: float,
        table: dict = {}
    ):
        """
        Initializes QLearner
        Args:
            learning_rate: float describing learning rate (between 0 and 1).
            discount_rate: float describing discount rate (between 0 and 1).
            discount_rate: float describing chance of taking random action (between 0 and 1).
        Returns:
            QLearner
        """
        super().__init__(learning_rate, discount_rate, random_chance, table)
        # YOUR CODE HERE


def get_state_from_args(request_args: dict) -> State:
    """
    Define how to map request arguments to a State.
    """
    # YOUR CODE HERE
    return State()


def get_action_from_args(request_args: dict) -> Action:
    """
    Define how to map request arguments to an Action.
    """
    # YOUR CODE HERE
    return Action()
