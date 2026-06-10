"""
随机过程数值模拟工具
纯 numpy 实现，不依赖 Manim，可单独测试
"""

import numpy as np


def simulate_bm(
    n_steps: int = 500,
    T: float = 1.0,
    n_paths: int = 1,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    模拟标准布朗运动（Wiener 过程）。

    原理：将 [0, T] 均分为 n_steps 段，每段增量
        ΔW_i ~ N(0, Δt)，即 sqrt(Δt) * Z，Z ~ N(0,1)
    路径由增量累加得到，W_0 = 0。

    Args:
        n_steps (int, optional): 时间步数. Defaults to 500.
        T (float, optional): 终止时间. Defaults to 1.0.
        n_paths (int, optional): 同时模拟的路径条数. Defaults to 1.
        seed (int | None, optional): 随机种子. Defaults to None.

    Returns:
        tuple[np.ndarray, np.ndarray]: 时间和路径数组
    """
    rng = np.random.default_rng(seed=seed)
    dt = T / n_steps

    # 增量矩阵：每一行一条路径，每列一个时间步
    increments = rng.normal(loc=0.0, scale=np.sqrt(dt), size=(n_paths, n_steps))

    # 最左边插一列 0，再做累加得到路径
    paths = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(increments, axis=1)], axis=1)

    t = np.linspace(0.0, T, n_steps + 1)
    return t, paths


def simulate_random_walk(
    n: int = 50,
    T: float = 1.0,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """模拟 Donsker 定理中的缩放随机游走。

    构造：X_i = ±1 等概率，缩放后
        S_n(t) = (1/√n) * Σ X_i，i = 1..⌊nt⌋
    当 n → ∞ 时依分布收敛到标准布朗运动。

    Args:
        n (int, optional): 步数（越大越接近布朗运动）. Defaults to 50.
        T (float, optional): 终止时间. Defaults to 1.0.
        seed (int | None, optional): 随机种子. Defaults to None.

    Returns:
        tuple[np.ndarray, np.ndarray]: _description_
    """
    rng = np.random.default_rng(seed)
    steps = rng.choice([-1.0, 1.0], size=n)
    path = np.concatenate([[0.0], np.cumsum(steps) / np.sqrt(n)])
    t = np.linspace(0.0, T, n + 1)
    return t, path


def simulate_markov_chain(
    P: np.ndarray,
    n_steps: int = 50,
    init_state: int = 0,
    seed: int | None = None,
) -> np.ndarray:
    """模拟离散时间马尔可夫链

    Args:
        P (np.ndarray): 转移矩阵，每行之和为1
        n_steps (int, optional): 模拟步数. Defaults to 50.
        init_state (int, optional): 出事状态索引. Defaults to 0.
        seed (int | None, optional): 随机种子. Defaults to None.

    Returns:
        np.ndarray: _description_
    """
    rng = np.random.default_rng(seed=seed)
    n_states = P.shape[0]
    states = np.empty(n_steps + 1, dtype=int)
    states[0] = init_state

    for i in range(n_steps):
        states[i + 1] = rng.choice(n_states, p=P[states[i]])

    return states
