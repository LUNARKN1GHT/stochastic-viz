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
    DIM_OPACITY,
    PATH_COLORS,
    PATH_STROKE,
)

N_STEPS = 800
T = 1.0
N_PATHS = 5
SEED = 42


class BrownianPath(Scene):
    def construct(self):

        # ── 标题 ────────────────────────────────────────────────────────────
        title = MathTex(r"W_t, \quad t \in [0,1]", color=AXIS_LABEL_COLOR)
        title.to_corner(UL)
        self.add(title)

        # ── 坐标轴 ──────────────────────────────────────────────────────────
        axes = Axes(
            x_range=[0, T, 0.25],
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

        # ── 模拟多条路径 ─────────────────────────────────────────────────────
        t, paths = simulate_bm(n_steps=N_STEPS, T=T, n_paths=N_PATHS, seed=SEED)

        path_mobs = []
        for k in range(N_PATHS):
            points = [axes.c2p(t[i], paths[k, i]) for i in range(len(t))]
            mob = VMobject(
                stroke_width=PATH_STROKE,
                color=PATH_COLORS[k % len(PATH_COLORS)],
            )
            mob.set_points_as_corners(points)
            path_mobs.append(mob)

        # 所有路径同时画出
        self.play(
            *[Create(m) for m in path_mobs],
            run_time=4,
            rate_func=linear,
        )

        # ── 压暗其他路径，高亮第一条 ─────────────────────────────────────────
        self.play(
            *[m.animate.set_opacity(DIM_OPACITY) for m in path_mobs[1:]],
            run_time=0.8,
        )
        self.wait(1)

        # 恢复所有路径
        self.play(
            *[m.animate.set_opacity(1.0) for m in path_mobs[1:]],
            run_time=0.8,
        )
        self.wait(0.5)
