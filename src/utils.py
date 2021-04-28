"""
Module for utilities.
"""
from copy import deepcopy
from typing import Any

import qrandom as qr


class Action:
    """Base class for actions."""

    def __init__(self, properties: Any = []):
        """Initialize state with a list of properties."""
        self.properties = properties
        self.name = 'Action'

    def __str__(self):
        """Return space separated string of properties."""
        x = str(self.properties)
        if type(self.properties) in [list, tuple]:
            x = ','.join([str(x) for x in self.properties])
        return f"{self.name}({x})"

    def __hash__(self) -> int:
        """Hashes the object."""
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        """Determines equality."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class State(Action):
    """Base class for states."""

    def __init__(self, properties: Any = (), terminal: bool = False):
        """
        Initialize state with a list of properties and
        bool describing whether or not state is terminal.
        """
        super().__init__(properties)
        self.terminal = terminal
        self.name = 'State'

    def next(self, action: Action = None):
        """
        Required method for getting next state, possibly given an action.
        Should only update the attributes of the class.
        """
        if self.terminal:
            return self
        return self

class QLearner:
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
        assert 0 <= learning_rate <= 1
        assert 0 <= discount_rate <= 1
        assert 0 <= random_chance <= 1

        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.random_chance = random_chance
        # YOUR CODE HERE
        self.possible_actions = []

        # Table to be of form {<str_state>: {..., <str_action_i>: <reward_i>, ...}}
        self.table = table

    def _init_state(self, state: State):
        """Initializes a string state in the Q table."""
        if state not in self.table:
            self.table[state] = {a: 0 for a in self.possible_actions}

    def get_action(self, state: State) -> Action:
        """
        Gets optimal action given a state.
        Args:
            state: State describing current state.
        Returns:
            Action
        """
        if qr.random() < self.random_chance:
            return qr.choice(self.possible_actions)
        if state in self.table:
            return max(self.table[state], key=self.table[state].get)
        self._init_state(state)
        return qr.choice(self.possible_actions)

    def update(self, state: State, action: Action, reward: float = 0):
        """
        Updates based on Q-Learning paradigm.
        Args:
            state: State describing current state.
            action: Action describing action taken given current state.
            reward: float associated with reward given from taking current action.
        """
        orig_state = deepcopy(state)
        state.next(action)
        next_state = deepcopy(state)
        if state.terminal:
            self.table[orig_state][action] = reward
            return
        self._init_state(orig_state)
        self._init_state(next_state)
        next_action = self.get_action(state)
        self.table[orig_state][action] = self.table[orig_state][action] + self.learning_rate * (
                reward + self.discount_rate * self.table[next_state][next_action]
                - self.table[orig_state][action]
        )
