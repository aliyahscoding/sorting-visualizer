# Sorting Algorithm Visualizer

![CI](https://github.com/aliyahscoding/sorting-visualizer/actions/workflows/ci.yml/badge.svg)

Python animation of classic sorting algorithms using Matplotlib `FuncAnimation`.

https://github.com/aliyahscoding/sorting-visualizer

## Demo

![Insertion Sort demo](reports/insertion_n40.gif)

## Features
- Algorithms: Insertion sort, Selection sort (easy to add more)
- CLI controls for size, algorithm, speed, and output format (GIF/MP4)
- Deterministic runs via `--seed`

## How to run

```bash
# Windows PowerShell (from repo root)
python src\visualize_sort.py --n 40 --algo insertion --speed 30 --format gif
python src\visualize_sort.py --n 60 --algo selection --speed 24 --format mp4

Outputs land in reports/.

Complexity
- Insertion sort: average/worst O(n^2), best O(n), in-place, stable
- Selection sort: always O(n^2), in-place, not stable (in general)