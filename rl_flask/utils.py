"""
Module for utilities.
To be used by utils_ext_base.py.
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List, Union

import qrandom as qr


class Action:
    """Base class for actions."""

    def __init__(self, properties: Any = None):
        """Initialize state with a list of properties."""
        self.properties = properties
        self.name = 'Action'

    def __eq__(self, other) -> bool:
        """Determines equality."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self) -> int:
        """Hashes the object."""
        return hash(self.__str__())

    def __str__(self):
        """Return space separated string of properties."""
        str_properties = str(self.properties)
        if type(self.properties) in [list, tuple]:
            str_properties = ','.join([str(property) for property in self.properties])
        return f"{self.name}({str_properties})"


class StateBase(ABC, Action):
    """Base class for states."""

    def __init__(self, properties: Any = None, terminal: bool = False):
        """
        Initialize state with a list of properties and
        bool describing whether or not state is terminal.
        """
        super().__init__(properties)
        self.properties = properties
        self.terminal = terminal
        self.name = 'State'

    @abstractmethod
    def next(self, action: Action = None):
        """
        Required method for getting next state, possibly given an action.
        Should only update the attributes of the class.
        """
        if self.terminal:
            return self
        return self

    @abstractmethod
    def reset(self):
        """Required method for resetting state to original state."""
        return self


class QLearner:
    """Class for Q Learning agent."""
    table: Dict[StateBase, Dict[Action, Union[float, int]]]

    def __init__(
        self,
        learning_rate: float,
        discount_rate: float,
        random_chance: float,
        possible_actions: List[Action],
    ):
        """
        Initializes QLearner
        Args:
            learning_rate: float describing learning rate (between 0 and 1).
            discount_rate: float describing discount rate (between 0 and 1).
            discount_rate: float describing chance of taking random action (between 0 and 1).
            possible_actions: List[Action] describing the list of possible actions.
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
        self.possible_actions = possible_actions

        # Table to be of form {<str_state>: {..., <str_action_i>: <reward_i>, ...}}
        self.table = {}

    def _init_state(self, state: StateBase):
        """Initializes a string state in the Q table."""
        if state not in self.table:
            self.table[state] = {a: 0 for a in self.possible_actions}

    def get_action(self, state: StateBase) -> Action:
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

    def update(self, state: StateBase, action: Action, reward: float = 0):
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
