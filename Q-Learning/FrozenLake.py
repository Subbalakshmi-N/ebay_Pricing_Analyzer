import numpy as np
import gym
import random
import matplotlib.pyplot as plt

env = gym.make("FrozenLake-v1", is_slippery=False)  # 4x4 grid, deterministic

state_size = env.observation_space.n   # Number of states (16)
action_size = env.action_space.n       # Number of actions (4: left, down, right, up)

# Initialize Q-table with zeros
Q_table = np.zeros((state_size, action_size))


learning_rate = 0.1    # α (How much to update Q-values)
discount_factor = 0.99  # γ (Importance of future rewards)
epsilon = 1.0          # ε (Initial exploration rate)
epsilon_decay = 0.995  # Decay rate (Reduce exploration over time)
epsilon_min = 0.01     # Minimum exploration rate
num_episodes = 2000    # Training episodes
max_steps = 100        # Max steps per episode

rewards_list = []  # To store total rewards per episode

for episode in range(num_episodes):
    state = env.reset()[0]  # Reset environment at the beginning of each episode
    total_reward = 0

    for step in range(max_steps):
        # Choose action (ε-greedy)
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Explore (random action)
        else:
            action = np.argmax(Q_table[state, :])  # Exploit (best known action)

        # Take action in environment
        next_state, reward, done, _, _ = env.step(action)

        # Q-Learning update rule
        Q_table[state, action] = Q_table[state, action] + learning_rate * (
                reward + discount_factor * np.max(Q_table[next_state, :]) - Q_table[state, action]
        )

        state = next_state
        total_reward += reward

        if done:  # Episode ends (goal reached or falls into hole)
            break

    # Decay exploration rate
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    rewards_list.append(total_reward)

    # Print progress every 100 episodes
    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {epsilon:.3f}")

print("Training completed!")

plt.plot(rewards_list)
plt.xlabel("Episodes")
plt.ylabel("Total Reward")
plt.title("Q-Learning Training Performance")
plt.show()

env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")
state = env.reset()[0]
total_reward = 0

for step in range(max_steps):
    action = np.argmax(Q_table[state, :])  # Always take best action
    next_state, reward, done, _, _ = env.step(action)
    total_reward += reward
    state = next_state

    if done:
        break

env.close()
print(f"Final Test Reward: {total_reward}")


