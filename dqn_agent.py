import tensorflow as tf
import numpy as np
import dqn_model
import experience_replay
import snake_game
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from consts import PIXEL, WINDOW_WIDTH, WINDOW_HEIGHT, Direction
from dqn_input import InputBuffer
global start_time, times

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, ROOT_DIR)


class DQNAgent:
    def __init__(self, num_states: int = 2, fps: int = 10, max_step: int = 1000):
        tf.compat.v1.reset_default_graph()
        self.num_states = num_states
        self.fps = fps

        self.model = dqn_model.SnakeDQN(num_states)
        self.saver = tf.compat.v1.train.Saver()
        self.session = tf.compat.v1.Session()
        self.state_buffer = InputBuffer(num_states)
        self.max_step = max_step
        self.sum_of_scores = 0
        self.mean_scores = []

    def load_model(self, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        self.saver.restore(self.session, save_path)

    def _save_model(self, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        self.saver.save(self.session, save_path)

    def _take_scores(self, i: int, num_steps: int, e: float, max_step: int, name: str):
        global start_time
        global times
        times = 1000
        if i % times == 0:  # print mean score of 100 episodes over all episodes
            mean = self.sum_of_scores / times
            self.mean_scores.append(mean)
            self.sum_of_scores = 0
            print("Episode: {0}, Score: {1}, Exploration: {2}, Max step: {3}".format(i, mean, e, max_step))
            self._save_model(name)

        if i % 100 == 0:
            end_time = datetime.now()
            time_difference = (end_time - start_time).total_seconds()
            print("Episode: {0} out of: {1} Episodes, Time: {2}".format(i, num_steps, time_difference))
            start_time = datetime.now()

    def train(self, num_steps: int = 100000, batch_size: int = 100,
              learning_rate: float = 0.0005, y: float = 0.9,
              start_e: float = 1.0, end_e: float = 0.01,
              start_max_step: int = 50, exploration_steps: int = 50000, save_name: str = None):

        global start_time

        game = snake_game.Snake(fps=self.fps)
        experience_buffer = experience_replay.ExperienceBuffer(
            state_shape=(WINDOW_WIDTH//PIXEL, WINDOW_HEIGHT//PIXEL, self.num_states))

        self.session.run(tf.compat.v1.global_variables_initializer())
        e = start_e
        step_optimizer = 0
        max_step = start_max_step
        start_time = datetime.now()
        for i in range(num_steps):
            if i <= exploration_steps:
                e -= (start_e - end_e) / exploration_steps
                step_optimizer += self.max_step / exploration_steps
                if step_optimizer >= 1 and max_step < self.max_step:
                    max_step += 1
                    step_optimizer -= 1

            game.config_parameters()
            self.state_buffer.zero_out_states()
            self.state_buffer.add_state(game.get_state_in_numpy_array())
            state = self.state_buffer.states
            step = 0
            while not (game.is_game_over() or step > max_step):
                step += 1
                if np.random.rand(1) <= e:  # exploration - random action
                    action = np.random.randint(0, 4)
                else:  # exploitation - let the model decide the action
                    action = self.session.run(self.model.predict_action,
                                              feed_dict={self.model.input: np.expand_dims(state, axis=0)})[0]
                action_dict = {
                    0: Direction.UP.value,
                    1: Direction.DOWN.value,
                    2: Direction.LEFT.value,
                    3: Direction.RIGHT.value
                }

                score = game.score
                game.ai_play(action_dict[action])

                if game.is_game_over():
                    self.state_buffer.add_state(np.zeros((WINDOW_WIDTH // PIXEL, WINDOW_HEIGHT // PIXEL)))
                    self.sum_of_scores += game.score
                    reward = -1
                else:
                    self.state_buffer.add_state(game.get_state_in_numpy_array())
                    reward = game.score - score  # if snake didn't eat then there is no reward, else r = 1

                state_next = self.state_buffer.states
                experience_buffer.add(state, action, reward, state_next, game.is_game_over())
                state = state_next

            if len(experience_buffer.buffer) >= batch_size:
                batch = experience_buffer.get_batch(batch_size)  # get new batch

                next_q = self.session.run(self.model.output_Q, feed_dict={self.model.input: batch['state_next']})
                target_q = self.session.run(self.model.output_Q, feed_dict={self.model.input: batch['state']})
                distance = 1 - batch['done'].reshape(batch_size)
                target_q[range(batch_size),
                         batch['action']] = batch['reward'] + y * distance * np.max(next_q, axis=1)  # bellman

                self.session.run(
                    self.model.update_model,
                    feed_dict={
                        self.model.input: batch['state'],
                        self.model.target_Q: target_q,
                        self.model.learning_rate: learning_rate})  # update model parameters

            self._take_scores(i, num_steps, e, max_step, save_name)

        if save_name is not None:
            self._save_model(save_name)
            self.plot_learning_curve(num_steps, save_name)

    def test(self):
        game = snake_game.Snake(fps=self.fps)
        game.config_parameters()
        steps = 0
        self.state_buffer.zero_out_states()
        while not game.is_game_over():
            state = game.get_state_in_numpy_array()
            self.state_buffer.add_state(state)
            states = self.state_buffer.states
            action = self.session.run(self.model.predict_action,
                                      feed_dict={self.model.input: np.expand_dims(states, axis=0)})[0]
            action_dict = {
                0: Direction.UP.value,
                1: Direction.DOWN.value,
                2: Direction.LEFT.value,
                3: Direction.RIGHT.value
            }
            action = action_dict[action]
            game.action = action

            print(action)
            game.ai_play(action)
            steps += 1

        print("Score: {0}, Steps: {1}".format(game.score, steps))
        return game.score

    def plot_learning_curve(self, num_steps: int, name: str):
        save_path = os.path.join(ROOT_DIR, 'trained_model', name)
        x_data = list(range(0, num_steps // times))
        y_data = self.mean_scores
        print(y_data)
        print(x_data)
        plt.plot(x_data, y_data)
        plt.title('Average score vs Episodes')
        plt.xlabel('Episodes (in ten thousands)')
        plt.ylabel('Score')
        plt.grid(True)
        plt.savefig(save_path)
        plt.show()

    def plot_test_histogram(self, test_num: int):
        scores = []
        for i in range(test_num):
            scores.append(self.test())
        scores.sort()

        plt.hist(scores, bins='auto')
        plt.xlabel('Score')
        plt.ylabel('Count')
        plt.title('Histogram of test scores')
        plt.grid(True)
        save_path = os.path.join(ROOT_DIR, 'trained_model', 'histogram')
        plt.savefig(save_path)
        plt.show()

        print("Max score: {0}, Min score: {1}, Average score: {2}".format(max(scores),
                                                                          min(scores), sum(scores) / len(scores)))


def main():
    agent = DQNAgent(fps=10, max_step=2000)
    # agent.train(save_name="15x10x100000x2000")
    agent.load_model("15x10x100000x2000")
    # agent.plot_test_histogram(100)
    agent.test()


if __name__ == '__main__':
    main()

