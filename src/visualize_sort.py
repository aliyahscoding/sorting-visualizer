# src/visualize_sort.py
# Usage examples:
#   python src\visualize_sort.py --n 40 --algo insertion --speed 30 --format gif
#   python src\visualize_sort.py --n 60 --algo selection --speed 24 --format mp4

import argparse
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# For MP4 without system-wide ffmpeg, we use imageio-ffmpeg.
import imageio_ffmpeg

from algorithms import insertion_sort_states, selection_sort_states


def make_data(n: int, seed: int | None = None) -> List[int]:
    rng = np.random.default_rng(seed)
    # permutation 1..n looks nicely "bar-charty"
    return (rng.permutation(n) + 1).tolist()

def colorize(n: int, state: Dict[str, Any]) -> List[str]:
    # Base color
    colors = ["tab:blue"] * n

    if "sorted" in state:
        for idx in state["sorted"]:
            if 0 <= idx < n:
                colors[idx] = "tab:green"

    if "min_idx" in state:
        mi = state["min_idx"]
        if 0 <= mi < n:
            colors[mi] = "tab:purple"

    if "active" in state:
        for idx in state["active"]:
            if 0 <= idx < n:
                colors[idx] = "tab:orange"

    if "compare" in state:
        for idx in state["compare"]:
            if 0 <= idx < n:
                colors[idx] = "tab:red"

    if "swap" in state:
        i, j = state["swap"]
        if 0 <= i < n:
            colors[i] = "black"
        if 0 <= j < n:
            colors[j] = "black"

    return colors

def build_frames(values: List[int], algo: str) -> List[Tuple[List[int], Dict[str, Any]]]:
    if algo == "insertion":
        gen = insertion_sort_states(values)
    elif algo == "selection":
        gen = selection_sort_states(values)
    else:
        raise ValueError(f"Unsupported algo: {algo}")
    return list(gen)

def animate(values: List[int], frames, fps: int, title: str, save_path: Path | None):
    n = len(values)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = list(range(n))
    bars = ax.bar(x, values, align="edge", width=0.8)

    ax.set_xlim(0, n)
    ax.set_ylim(0, max(values) * 1.15)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title(title)

    txt = ax.text(0.02, 0.95, "", transform=ax.transAxes, va="top", ha="left")

    def update(frame):
        arr, state = frame
        # heights
        for bar, h in zip(bars, arr):
            bar.set_height(h)
        # colors
        cols = colorize(n, state)
        for bar, c in zip(bars, cols):
            bar.set_color(c)
        # info text
        info = state.get("info", "")
        txt.set_text(info)
        return (*bars, txt)

    interval_ms = int(1000 / max(1, fps))
    ani = FuncAnimation(fig, update, frames=frames, interval=interval_ms, blit=False, repeat=False)

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        ext = save_path.suffix.lower()
        if ext == ".gif":
            writer = PillowWriter(fps=fps)
            ani.save(save_path.as_posix(), writer=writer)
        elif ext == ".mp4":
            # Point Matplotlib to an ffmpeg binary via imageio-ffmpeg
            plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
            from matplotlib.animation import FFMpegWriter
            writer = FFMpegWriter(fps=fps, bitrate=1800)
            ani.save(save_path.as_posix(), writer=writer)
        else:
            raise ValueError("Use .gif or .mp4 for --out (or set --format)")

    # Close the figure so headless runs don't pop a window
    plt.close(fig)

def main():
    p = argparse.ArgumentParser(description="Sorting Visualizer")
    p.add_argument("--n", type=int, default=40, help="number of bars")
    p.add_argument("--algo", type=str, default="insertion", choices=["insertion", "selection"], help="algorithm")
    p.add_argument("--speed", type=int, default=30, help="frames per second")
    p.add_argument("--format", type=str, default="gif", choices=["gif", "mp4"], help="output format")
    p.add_argument("--out", type=str, default="", help="custom output path; overrides --format if extension given")
    p.add_argument("--seed", type=int, default=42, help="random seed for reproducibility")
    args = p.parse_args()

    values = make_data(args.n, seed=args.seed)
    frames = build_frames(values, args.algo)

    # Output file path
    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path("reports") / f"{args.algo}_n{args.n}.{args.format}"

    title = f"{args.algo.title()} Sort | n={args.n} | {args.format.upper()} @ {args.speed}fps"
    animate(values, frames, fps=args.speed, title=title, save_path=out_path)

    print(f"Saved animation to: {out_path}")

if __name__ == "__main__":
    main()
