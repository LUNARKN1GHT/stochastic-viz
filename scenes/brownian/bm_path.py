"""
标准布朗运动路径可视化。

运行：
    manim -pql scenes/brownian/bm_path.py BrownianPath
"""

from manim import *

from utils.simulation import simulate_bm
from utils.style import (
    AXIS_COLOR,
    AXIS_LABEL_COLOR,
    AXIS_STROKE,
    PATH_COLORS,
    PATH_STROKE,
)

# 模拟参数
N_STEPS = 800
T = 1.0
SEED = 42


class BrownianPath(Scene):
    def construct(self):

        # ── 标题 ────────────────────────────────────────────────────────────
        title = MathTex(r"W_t, \quad t \in [0,1]", color=AXIS_LABEL_COLOR)
        title.to_corner(UL)
        self.add(title)

        # ── 坐标轴 ──────────────────────────────────────────────────────────
        axes = Axes(
            x_range=[0, T, 0.25],  # [最小值, 最大值, 刻度间隔]
            y_range=[-2.5, 2.5, 1.0],
            x_length=10,
            y_length=5,
            axis_config={
                "color": AXIS_COLOR,
                "stroke_width": AXIS_STROKE,
                "include_ticks": True,
            },
        )
        x_label = axes.get_x_axis_label(MathTex("t", color=AXIS_LABEL_COLOR), edge=RIGHT)
        y_label = axes.get_y_axis_label(MathTex("W_t", color=AXIS_LABEL_COLOR), edge=UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # ── 模拟并转换坐标 ───────────────────────────────────────────────────
        t, paths = simulate_bm(n_steps=N_STEPS, T=T, n_paths=1, seed=SEED)

        # axes.c2p(x, y) 把数据坐标 → Manim 场景坐标（canvas position）
        points = [axes.c2p(t[i], paths[0, i]) for i in range(len(t))]

        # set_points_as_corners：折线连接，保留锯齿感（布朗运动不光滑）
        path_mob = VMobject(stroke_width=PATH_STROKE, color=PATH_COLORS[0])
        path_mob.set_points_as_corners(points)

        # ── 动画：路径从左向右逐步画出 ───────────────────────────────────────
        self.play(Create(path_mob), run_time=4, rate_func=linear)
        self.wait(1)
