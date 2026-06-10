"""
马尔可夫链状态转移图可视化。

运行：
    manim -pqm scenes/markov/transition_graph.py TransitionGraph
"""

import numpy as np
from manim import *

from utils.style import (
    AXIS_LABEL_COLOR,
    GUIDE_COLOR,
    HIGHLIGHT_COLOR,
    PATH_COLORS,
    PATH_STROKE,
)

# 转移矩阵：3 个状态
P = np.array(
    [
        [0.7, 0.2, 0.1],
        [0.3, 0.5, 0.2],
        [0.1, 0.4, 0.5],
    ]
)

# 状态标签与节点位置（场景坐标）
STATE_LABELS = ["0", "1", "2"]
STATE_POSITIONS = [LEFT * 3, UP * 2, RIGHT * 3]


class TransitionGraph(Scene):
    def construct(self):

        # ── 标题 ────────────────────────────────────────────────────────────
        title = Text("马尔可夫链：状态转移图", font_size=32, color=AXIS_LABEL_COLOR)
        title.to_corner(UL)
        self.play(Write(title))

        # ── 绘制节点 ─────────────────────────────────────────────────────────
        nodes = []
        for i, (label, pos) in enumerate(zip(STATE_LABELS, STATE_POSITIONS, strict=True)):
            circle = Circle(radius=0.5, color=PATH_COLORS[i], stroke_width=2.5)
            circle.move_to(pos)
            text = MathTex(label, color=AXIS_LABEL_COLOR, font_size=36)
            text.move_to(pos)
            nodes.append(VGroup(circle, text))

        self.play(*[Create(n) for n in nodes])

        # ── 绘制转移边 ───────────────────────────────────────────────────────
        # 自环用 CurvedArrow 画一个小圈；跨节点用 CurvedArrow 避免重叠
        def make_edge(i: int, j: int, prob: float) -> VGroup:
            start = STATE_POSITIONS[i]
            end = STATE_POSITIONS[j]
            color = GUIDE_COLOR

            if i == j:
                # 自环：在节点正上方/正下方画弧
                offset = UP * 1.1 if i != 1 else DOWN * 1.1
                arrow = CurvedArrow(
                    start + offset * 0.4,
                    start + offset * 0.4 + RIGHT * 0.01,  # 起终点几乎重合
                    angle=TAU * 0.7,
                    color=color,
                    stroke_width=PATH_STROKE,
                )
                label_pos = start + offset * 1.15
            else:
                # 跨节点：稍微弯曲避免正反向箭头重叠
                arrow = CurvedArrow(
                    start,
                    end,
                    angle=0.3,
                    color=color,
                    stroke_width=PATH_STROKE,
                )
                label_pos = (start + end) / 2 + np.cross(end - start, OUT) * 0.25

            prob_label = MathTex(f"{prob:.1f}", font_size=24, color=AXIS_LABEL_COLOR).move_to(
                label_pos
            )

            return VGroup(arrow, prob_label)

        edges = []
        for i in range(len(STATE_LABELS)):
            for j in range(len(STATE_LABELS)):
                if P[i, j] > 0:
                    edges.append(make_edge(i, j, P[i, j]))

        self.play(*[Create(e) for e in edges], run_time=2)
        self.wait(1)

        # ── 高亮一条路径：0 → 1 → 2 ─────────────────────────────────────────
        highlight_path = [0, 1, 2]
        for k in range(len(highlight_path)):
            idx = highlight_path[k]
            self.play(
                nodes[idx][0].animate.set_color(HIGHLIGHT_COLOR),
                run_time=0.5,
            )
            self.wait(0.4)

        self.wait(1)
