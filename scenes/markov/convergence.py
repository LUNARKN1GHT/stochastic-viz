"""
转移矩阵幂次收敛到平稳分布可视化。

运行：
    manim -pqm scenes/markov/convergence.py MarkovConvergence

参考：
    Ross《随机过程》第 4 章 4.3-4.4 节（极限定理、平稳分布）
"""

import numpy as np
from manim import *

from utils.simulation import stationary_distribution
from utils.style import (
    AXIS_LABEL_COLOR,
    HIGHLIGHT_COLOR,
    PATH_COLORS,
)

P = np.array(
    [
        [0.7, 0.2, 0.1],
        [0.3, 0.5, 0.2],
        [0.1, 0.4, 0.5],
    ]
)

STATE_LABELS = ["0", "1", "2"]
# 展示的幂次序列
N_SEQUENCE = [1, 2, 5, 10, 20, 50]


def fmt(x: float) -> str:
    """将概率格式化为两位小数字符串。"""
    return f"{x:.2f}"


class MarkovConvergence(Scene):
    def construct(self):

        # ── 标题 ────────────────────────────────────────────────────────────
        title = Text("P^n 收敛到平稳分布 π", font_size=30, color=AXIS_LABEL_COLOR)
        title.to_corner(UL)
        self.play(Write(title))

        pi = stationary_distribution(P)

        # ── 左侧：矩阵显示 ───────────────────────────────────────────────────
        def make_matrix_mob(Pn: np.ndarray, n: int) -> VGroup:
            """生成 P^n 的矩阵 Mobject。"""
            rows = []
            for i in range(3):
                row = [fmt(Pn[i, j]) for j in range(3)]
                rows.append(row)

            mat = Matrix(rows, element_to_mobject_config={"font_size": 28})
            mat.set_color(AXIS_LABEL_COLOR)

            label = MathTex(rf"P^{{{n}}}", font_size=36, color=PATH_COLORS[0])
            label.next_to(mat, UP, buff=0.3)

            group = VGroup(label, mat)
            group.move_to(LEFT * 3.5)
            return group

        # ── 右侧：条形图（每行一组，3 行 × 3 状态）───────────────────────────
        def make_bars(Pn: np.ndarray) -> VGroup:
            """
            为 P^n 的每一行生成概率条形图。
            每行对应一个初始状态，3 根柱子对应 3 个目标状态。
            """
            bar_width = 0.25
            bar_gap = 0.15
            row_gap = 0.6
            max_height = 1.8
            origin = RIGHT * 1.5 + DOWN * 2.0

            all_bars = VGroup()
            for i in range(3):
                for j in range(3):
                    h = Pn[i, j] * max_height
                    bar = Rectangle(
                        width=bar_width,
                        height=max(h, 0.01),
                        fill_color=PATH_COLORS[j],
                        fill_opacity=0.85,
                        stroke_width=0,
                    )
                    x = j * (bar_width + bar_gap)
                    y = i * (max_height + row_gap)
                    bar.move_to(origin + RIGHT * x + UP * y, aligned_edge=DOWN)
                    all_bars.add(bar)

            # 行标签（初始状态）
            for i in range(3):
                y = i * (max_height + row_gap)
                lbl = MathTex(rf"i={i}", font_size=24, color=AXIS_LABEL_COLOR).move_to(
                    origin + LEFT * 0.5 + UP * (y + max_height / 2)
                )
                all_bars.add(lbl)

            # 平稳分布参考线
            for i in range(3):
                y = i * (max_height + row_gap)
                for j in range(3):
                    ref_h = pi[j] * max_height
                    x = j * (bar_width + bar_gap)
                    line = DashedLine(
                        start=origin + RIGHT * (x - bar_width / 2) + UP * (y + ref_h),
                        end=origin + RIGHT * (x + bar_width / 2) + UP * (y + ref_h),
                        color=HIGHLIGHT_COLOR,
                        stroke_width=1.5,
                    )
                    all_bars.add(line)

            return all_bars

        # ── 初始显示 n=1 ────────────────────────────────────────────────────
        Pn = P.copy()
        mat_mob = make_matrix_mob(Pn, 1)
        bars_mob = make_bars(Pn)

        self.play(Write(mat_mob), Create(bars_mob), run_time=1.5)
        self.wait(0.5)

        # ── 逐步更新 ─────────────────────────────────────────────────────────
        for n in N_SEQUENCE[1:]:
            Pn = np.linalg.matrix_power(P, n)
            new_mat = make_matrix_mob(Pn, n)
            new_bars = make_bars(Pn)

            self.play(
                Transform(mat_mob, new_mat),
                Transform(bars_mob, new_bars),
                run_time=1.0,
            )
            self.wait(0.6)

        # ── 最终标注平稳分布 ─────────────────────────────────────────────────
        pi_label = MathTex(
            rf"\pi = ({fmt(pi[0])},\, {fmt(pi[1])},\, {fmt(pi[2])})",
            font_size=30,
            color=HIGHLIGHT_COLOR,
        ).to_corner(DR)
        self.play(Write(pi_label))
        self.wait(1.5)
