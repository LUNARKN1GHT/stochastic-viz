"""
Donsker 定理可视化：缩放随机游走收敛到布朗运动。

运行：
    manim -pqk scenes/brownian/random_walk_limit.py RandomWalkLimit
"""

from manim import *

from utils.simulation import simulate_bm, simulate_random_walk
from utils.style import (
    AXIS_COLOR,
    AXIS_LABEL_COLOR,
    AXIS_STROKE,
    HIGHLIGHT_COLOR,
    PATH_COLORS,
    PATH_STROKE,
)

T = 1.0
# 依次演示的步数：从粗糙到精细
N_SEQUENCE = [10, 50, 200, 1000]
SEED = 7


class RandomWalkLimit(Scene):
    def construct(self):

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
        y_label = axes.get_y_axis_label(MathTex("S_n(t)", color=AXIS_LABEL_COLOR), edge=UP)
        self.play(Create(axes), Write(x_label), Write(y_label))

        # ── 步数标签 ─────────────────────────────────────────────────────────
        n_label = always_redraw(lambda: Text("", font_size=28))  # 占位，下面替换
        n_label = MathTex(r"n = 10", color=AXIS_LABEL_COLOR, font_size=36)
        n_label.to_corner(UR)
        self.add(n_label)

        # ── 第一条随机游走 ───────────────────────────────────────────────────
        t, path = simulate_random_walk(n=N_SEQUENCE[0], T=T, seed=SEED)
        points = [axes.c2p(t[i], path[i]) for i in range(len(t))]
        walk_mob = VMobject(stroke_width=PATH_STROKE + 0.5, color=PATH_COLORS[0])
        walk_mob.set_points_as_corners(points)
        self.play(Create(walk_mob), run_time=1.5, rate_func=linear)

        # ── 依次变换到更密的随机游走 ─────────────────────────────────────────
        for n in N_SEQUENCE[1:]:
            t_new, path_new = simulate_random_walk(n=n, T=T, seed=SEED)
            points_new = [axes.c2p(t_new[i], path_new[i]) for i in range(len(t_new))]
            new_mob = VMobject(stroke_width=PATH_STROKE + 0.5, color=PATH_COLORS[0])
            new_mob.set_points_as_corners(points_new)

            new_label = MathTex(rf"n = {n}", color=AXIS_LABEL_COLOR, font_size=36)
            new_label.to_corner(UR)

            self.play(
                Transform(walk_mob, new_mob),
                Transform(n_label, new_label),
                run_time=1.5,
            )
            self.wait(0.5)

        # ── 叠加真正的布朗运动路径对比 ───────────────────────────────────────
        _, bm_paths = simulate_bm(n_steps=800, T=T, n_paths=1, seed=SEED)
        bm_points = [axes.c2p(i / 800, bm_paths[0, i]) for i in range(801)]
        bm_mob = VMobject(stroke_width=PATH_STROKE, color=HIGHLIGHT_COLOR)
        bm_mob.set_points_as_corners(bm_points)

        bm_label = MathTex(r"W_t", color=HIGHLIGHT_COLOR, font_size=36)
        bm_label.next_to(n_label, DOWN, buff=0.2)

        self.play(Create(bm_mob), Write(bm_label), run_time=2, rate_func=linear)
        self.wait(1.5)
