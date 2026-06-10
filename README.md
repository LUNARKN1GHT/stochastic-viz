# stochastic-viz

Animated visualizations of stochastic processes, built with [Manim](https://www.manim.community/).

Learning path: **Ross — Stochastic Processes** → **Shreve — Stochastic Calculus for Finance**.

## Structure

```text
scenes/
├── markov/    # Discrete & continuous-time Markov chains
├── poisson/   # Poisson process
├── ctmc/      # Continuous-time Markov chains
├── brownian/  # Brownian motion
├── ito/       # Ito calculus & SDEs
└── binomial/  # Binomial asset pricing model
utils/
├── simulation.py   # Numerical simulation helpers
└── style.py        # Shared color palette & stroke widths
```

Book references (Ross / Shreve chapter) are noted in each scene file's docstring.

## Setup

**With uv (recommended):**

```bash
uv venv
uv pip install -e ".[dev]"
```

**With conda:**

```bash
conda create -n stochastic-viz python=3.11
conda activate stochastic-viz
pip install -e ".[dev]"
```

Manim also requires system dependencies (Cairo, FFmpeg, LaTeX).
See the [Manim installation guide](https://docs.manim.community/en/stable/installation.html).

## Rendering a scene

```bash
# Low quality (fast preview)
manim -pql scenes/ross/ch08_brownian/brownian_paths.py BrownianPaths

# High quality
manim -pqh scenes/ross/ch08_brownian/brownian_paths.py BrownianPaths
```

Output is written to `media/` (gitignored).

## License

MIT
