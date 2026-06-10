"""
Shared color palette and Manim style constants.
Import these in every scene to keep visuals consistent.
"""

from manim import ManimColor

# Path colors for multi-path plots
PATH_COLORS: list[ManimColor] = [
    ManimColor("#4C9BE8"),  # blue
    ManimColor("#E8754C"),  # orange
    ManimColor("#4CE87A"),  # green
    ManimColor("#E84C4C"),  # red
    ManimColor("#B04CE8"),  # purple
]

# Highlight / annotation
HIGHLIGHT = ManimColor("#FFD166")
AXIS_COLOR = ManimColor("#AAAAAA")

# Stroke widths
PATH_STROKE = 2.5
THIN_STROKE = 1.5
