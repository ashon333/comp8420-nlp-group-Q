# COMP8430 – Advanced Computer Vision and Action
## Assessment Task 1: Reinforcement Learning Programming Assignment

> **Unit:** COMP8430 — Advanced Computer Vision and Action  
> **Institution:** Macquarie University  
> **Session:** 2026 Session 1  
> **Due:** 29 May 2026  
> **Weight:** 30% of overall unit grade

---

## Overview

This repository contains the Jupyter Notebook submission for Assessment Task 1. The assignment implements and evaluates several reinforcement learning (RL) agents across four progressively complex environments, covering tabular Q-learning, deep RL with neural networks, pixel-based learning, and custom environment design.

---

## Repository Structure

```
.
├── notebook.ipynb      ← Main submission (run all cells top-to-bottom)
└── README.md           ← This file
```

> **Note:** The notebook is self-contained. No additional data files or model checkpoints are required or included, in accordance with submission instructions.

---

## Tasks Summary

| Task | Topic | Environment | Algorithm(s) | Marks |
|------|-------|-------------|--------------|-------|
| 1 | Tabular Q-learning | Taxi-v3 | Q-learning (ε-greedy) | 5 |
| 2 | Deep RL on vector obs | LunarLander-v3 | DQN vs PPO | 10 |
| 3 | RL from pixels | AirRaidNoFrameskip-v4 | PPO + CNN | 10 |
| 4 | Custom environment | MountainCar-v0 (wrapped) | PPO + reward shaping | 5 |

---

## Task Details

### Task 1 – Q-learning on Taxi-v3
- Implements tabular Q-learning from scratch using NumPy
- Trains two agents with different epsilon decay rates: **0.002** and **0.006**
- Evaluates the greedy policy every **500 training steps** using **30 episodes**
- Produces one convergence plot per decay rate showing mean accumulated reward
- Environment: [`Taxi-v3`](https://gymnasium.farama.org/environments/toy_text/taxi/) — 500 discrete states, 6 actions

### Task 2 – DQN vs PPO on LunarLander-v3
- Compares convergence of **DQN** (off-policy, experience replay) and **PPO** (on-policy, clipped surrogate objective)
- Both implemented via [Stable Baselines 3](https://stable-baselines3.readthedocs.io/)
- Evaluates every **2,000 training steps** using **25 episodes**; separate plot per algorithm
- Environment: [`LunarLander-v3`](https://gymnasium.farama.org/environments/box2d/lunar_lander/) — 8-dim continuous obs, 4 discrete actions; solved at ≥200 reward

### Task 3 – PPO from Pixels on AirRaid (Atari)
- Trains PPO with a **convolutional neural network** (`CnnPolicy`) on raw pixel observations
- Custom preprocessing wrappers: grayscale + resize to 84×84, frame skipping, frame stacking
- Two experimental conditions compared:
  - **Condition A:** frame skip = 6, frame stack = 3 → input shape `(3, 84, 84)`
  - **Condition B:** no skip, no stack → input shape `(1, 84, 84)`
- Evaluates every **5,000 steps** using **20 episodes** capped at **1,000 steps each**
- Environment: [`AirRaidNoFrameskip-v4`](https://ale.farama.org/environments/air_raid/)

### Task 4 – Custom MountainCar Environments
- Wraps `MountainCar-v0` with two distinct shaped reward functions to overcome sparse rewards:
  - **Reward 1 (Position-based):** `default + position_weight × max(0, pos + 0.5) + goal_bonus`
  - **Reward 2 (Energy-based):** `default + velocity_weight × |vel| + height_weight × (pos + 1.2) + goal_bonus`
- Both environments inherit `gym.Env` (matching the assignment starter code pattern)
- Trains PPO on each; evaluates on the **original** sparse-reward environment
- Reports mean reward and goal success rate; includes a per-episode demonstration plot
- Environment: [`MountainCar-v0`](https://gymnasium.farama.org/environments/classic_control/mountain_car/)

---

## Setup & Installation

### Requirements
- Python 3.8+
- `swig` (required by `gymnasium[box2d]`) — install via system package manager or pip

### Install all dependencies

Run the first code cell in `notebook.ipynb`, or install manually:

```bash
pip install swig
pip install "gymnasium[toy-text]"
pip install "gymnasium[box2d]"
pip install "gymnasium[atari]"
pip install "gymnasium[accept-rom-license]"
pip install ale-py
pip install "stable-baselines3[extra]"
pip install "shimmy>=0.2.0"
pip install opencv-python matplotlib torch
```

### If `gymnasium[box2d]` fails to install
Box2D requires `swig`. See the [StackOverflow fix](https://stackoverflow.com/questions/51811263/problems-pip-installing-box2d) referenced in the assignment description.

---

## Running the Notebook

1. Install dependencies (see above)
2. Open `notebook.ipynb` in JupyterLab or Jupyter Notebook
3. **Run all cells top-to-bottom** (`Kernel → Restart & Run All`)
4. All outputs and plots will be generated inline

> ⚠️ Tasks 3 (Atari, 2M steps) is compute-intensive. A GPU is recommended but not required. Expected runtimes on CPU: Task 1 ~5 min, Task 2 ~30 min, Task 3 ~2–4 hrs, Task 4 ~10 min.

---

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `gymnasium` | RL environments (Taxi, LunarLander, Atari, MountainCar) |
| `stable-baselines3` | DQN and PPO implementations (used in unit practicals) |
| `ale-py` | Atari Learning Environment backend |
| `opencv-python` | Frame preprocessing (grayscale, resize) |
| `torch` | Neural network backend for SB3 |
| `numpy` / `matplotlib` | Numerics and plotting |

---

## Implementation Notes

- **Tabular Q-learning (Task 1):** Implemented from scratch using NumPy. Epsilon is decayed multiplicatively after each episode. Evaluation triggers on training step count, not episode count.
- **SB3 (Tasks 2–4):** Stable Baselines 3 is used consistent with the unit's practical sessions. `MlpPolicy` is used for vector observations; `CnnPolicy` for image observations.
- **Atari wrappers (Task 3):** Custom `GrayscaleResize84`, `MaxFrameSkip`, and `FrameStack` wrappers implement the standard preprocessing pipeline from Mnih et al. (2015).
- **Custom environments (Task 4):** Both classes inherit `gym.Env` and explicitly declare `action_space`, `observation_space`, `reset()`, `step()`, `render()`, and `close()`, following the assignment starter code pattern.
- **Evaluation integrity (Task 4):** The `MCEvalCallback` evaluates on the original unmodified `MountainCar-v0` (sparse reward) to measure true task completion, not inflated shaped rewards.

---

## Use of AI

Generative AI (Claude, Anthropic) was used to assist with code scaffolding. Full disclosure of tools, prompts, components, and modifications is provided in the **"Use of AI Generators in this Assignment"** section at the end of `notebook.ipynb`, as required by the unit's open AI policy.

---

## References

- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning.* Nature, 518, 529–533.
- Schulman, J. et al. (2017). *Proximal Policy Optimization Algorithms.* arXiv:1707.06347.
- Ng, A. Y., Harada, D., & Russell, S. (1999). *Policy invariance under reward transformations: Theory and application to reward shaping.* ICML.
- Dietterich, T. G. (2000). *Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition.* JAIR, 13, 227–303.
- Farama Foundation. Gymnasium Documentation. https://gymnasium.farama.org/
- Stable Baselines 3 Documentation. https://stable-baselines3.readthedocs.io/
