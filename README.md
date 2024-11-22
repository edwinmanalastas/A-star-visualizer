# A* Pathfinding Algorithm Visualizer

## Overview
A visual tool to demonstrate the A* Pathfinding Algorithm using Python and Pygame. Users can create grids, set start/end nodes, add barriers, and visualize the shortest path in real-time.<br/>
**Algorithm**: Uses Manhattan distance for heuristic and backtracks to show the shortest path.


## Features
- Interactive grid creation.
- Real-time pathfinding visualization.
- Reset functionality.
- Keyboard and mouse controls.

## Requirements
- Python 3.8+
- Pygame (`pip install pygame`)

## How to Run
1. Install Pygame:
   ```bash
   pip install pygame
   ```
2. Run the script:
   ```bash
   python main.py
   ```
## Controls
| Action                | Control         |
|-----------------------|-----------------|
| Place start node      | Left-click      |
| Place end node        | Left-click      |
| Add/remove barriers   | Left/right-click|
| Start algorithm       | Press `SPACE`  |
| Reset grid            | Press `C`      |
