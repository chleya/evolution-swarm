# Test game import
import sys
sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace\edge_swarm_system")
from all_games_improved import Maze, Predator

# Test
m = Maze()
print(f"Maze game loaded: {m.NAME}")

p = Predator()
print(f"Predator game loaded: {p.NAME}")
