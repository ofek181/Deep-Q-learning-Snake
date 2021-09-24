import numpy as np
import random


class ExperienceBuffer:
    def __init__(self, state_shape: tuple, buffer_size: int = 10000):
        self.buffer = []
        self.state_shape = state_shape
        self.buffer_size = buffer_size

    def add(self, state: np.array, action: str, reward: int, state_next: np.array, done: bool):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)

        experience = np.concatenate([
            state.flatten(),
            np.array(action).flatten(),
            np.array(reward).flatten(),
            state_next.flatten(),
            np.array(int(done)).flatten()
        ])
        self.buffer.append(experience)  # experience buffer as mention in books

    def get_batch(self, size: int) -> dict:
        batch_size = min(len(self.buffer), size)
        state_size = np.prod(self.state_shape)

        experiences = np.array(random.sample(self.buffer, batch_size)) # sampling some experiences

        batch = {'state': experiences[:, :state_size].reshape((batch_size,) + self.state_shape),
                 'action': np.cast['int'](experiences[:, state_size]),
                 'reward': experiences[:, state_size + 1],
                 'state_next': experiences[:, state_size + 2:2 * state_size + 2].reshape(
                     (batch_size,) + self.state_shape),
                 'done': experiences[:, 2 * state_size + 2]}
        return batch
