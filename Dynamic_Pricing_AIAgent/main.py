import numpy as np
import pandas as pd
import xgboost as xgb
import gym
import torch
import torch.nn as nn
import torch.optim as optim
from stable_baselines3 import PPO
from fastapi import FastAPI
import random
import requests

# Step 1: Supervised Fine-Tuning (SFT) - Train XGBoost on historical pricing data

data = {
    "competitor_price": np.random.uniform(50, 150, 1000),
    "demand_trend": np.random.uniform(0.5, 1.5, 1000),
    "stock_level": np.random.randint(10, 500, 1000),
    "past_price": np.random.uniform(60, 140, 1000),
}

data["optimal_price"] = data["past_price"] * data["demand_trend"] * 0.9 + np.random.uniform(-5, 5, 1000)
df = pd.DataFrame(data)

X = df.drop(columns=["optimal_price"])
y = df["optimal_price"]

sft_model = xgb.XGBRegressor(objective="reg:squarederror")
sft_model.fit(X, y)


# Step 2: Reinforcement Learning (RL) - Define the AI Agent
class PricingEnv(gym.Env):
    def __init__(self):
        super(PricingEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(3)  # Actions: Decrease (-5%), Hold, Increase (+5%)
        self.observation_space = gym.spaces.Box(low=0, high=200, shape=(4,), dtype=np.float32)
        self.state = self._reset()

    def _reset(self):
        self.state = np.array(
            [random.uniform(50, 150), random.uniform(0.5, 1.5), random.randint(10, 500), random.uniform(60, 140)])
        return self.state

    def step(self, action):
        competitor_price, demand_trend, stock_level, past_price = self.state

        if action == 0:
            new_price = past_price * 0.95
        elif action == 1:
            new_price = past_price
        else:
            new_price = past_price * 1.05

        revenue = new_price * demand_trend if new_price < competitor_price else new_price * (demand_trend - 0.1)
        reward = revenue - (new_price * 0.3)

        self.state = np.array([competitor_price, demand_trend, stock_level, new_price])
        return self.state, reward, False, {}


pricing_env = PricingEnv()
ppo_agent = PPO("MlpPolicy", pricing_env, verbose=1)
ppo_agent.learn(total_timesteps=10000)

# Step 3: FastAPI Deployment for Real-time Pricing
app = FastAPI()


@app.get("/predict_price")
def predict_price(demand_trend: float, stock_level: int, past_price: float):
    competitor_price = random.uniform(50, 150)  # Simulated competitor price
    input_data = np.array([[competitor_price, demand_trend, stock_level, past_price]])
    predicted_price = sft_model.predict(input_data)[0]
    return {"competitor_price": competitor_price, "recommended_price": round(predicted_price, 2)}


@app.post("/update_price")
def auto_update_price(demand_trend: float, stock_level: int, past_price: float):
    state = np.array([random.uniform(50, 150), demand_trend, stock_level, past_price])
    action, _ = ppo_agent.predict(state)

    if action == 0:
        new_price = past_price * 0.95
    elif action == 1:
        new_price = past_price
    else:
        new_price = past_price * 1.05

    return {"updated_price": round(new_price, 2)}


# Step 4: Continuous Learning (Logging and Updating Model in Production)
# (To be implemented in future iterations)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
