"""
共享样式常量：颜色、线宽、透明度。
所有 scene 文件从这里导入，不在 scene 里硬编码颜色。
"""

from manim import ManimColor

# --- 主色板 -----------
# 路径颜色：多条路径时依次取用
PATH_COLORS: list[ManimColor] = [
    ManimColor("#4FC3F7"),  # 浅蓝
    ManimColor("#EF9A9A"),  # 浅红
    ManimColor("#A5D6A7"),  # 浅绿
    ManimColor("#FFE082"),  # 浅黄
    ManimColor("#CE93D8"),  # 浅紫
]

# 坐标轴
AXIS_COLOR = ManimColor("#B0BEC5")  # 蓝灰
AXIS_LABEL_COLOR = ManimColor("#ECEFF1")  # 近白

# 辅助线 / 标注
GUIDE_COLOR = ManimColor("#78909C")  # 深蓝灰
HIGHLIGHT_COLOR = ManimColor("#FFD54F")  # 琥珀，用于重点标注

# 背景（与 manim 默认黑色背景搭配）
BG_COLOR = ManimColor("#0D0D0D")

# ── 线宽 ────────────────────────────────────────────────
PATH_STROKE = 2.0  # 随机过程路径
AXIS_STROKE = 1.5  # 坐标轴
GUIDE_STROKE = 1.0  # 辅助线

# ── 透明度 ──────────────────────────────────────────────
DIM_OPACITY = 0.3  # 次要路径（多路径时压暗背景路径）
