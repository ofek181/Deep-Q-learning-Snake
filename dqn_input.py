import numpy as np
from consts import PIXEL, WINDOW_WIDTH, WINDOW_HEIGHT


class InputBuffer:
    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size
        self.states = np.zeros((WINDOW_WIDTH // PIXEL, WINDOW_HEIGHT // PIXEL, self.buffer_size))
        self.zero_out_states()

    def zero_out_states(self):
        self.states = np.zeros((WINDOW_WIDTH // PIXEL, WINDOW_HEIGHT // PIXEL, self.buffer_size))

    def add_state(self, state: np.array):
        state_expanded = np.expand_dims(state, axis=-1)
        self.states = np.concatenate((state_expanded, self.states), axis=-1)
        self.states = np.delete(self.states, -1, -1)

