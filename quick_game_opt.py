# -*- coding: utf-8 -*-
"""
Quick Game Optimizer - 快速游戏参数优化
简化版，用于快速验证
"""

import random
import torch
import sys
sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace\edge_swarm_system")
from all_games_improved import *


class QuickOptimizer:
    """快速优化器"""
    
    def __init__(self, game_class, genome_schema, episodes=20):
        self.game_class = game_class
        self.genome_schema = genome_schema
        self.episodes = episodes
    
    def random_search(self, iterations=50):
        """随机搜索"""
        best_genome = None
        best_fitness = -float('inf')
        
        for i in range(iterations):
            genome = {}
            for key, config in self.genome_schema.items():
                if config['type'] == 'int':
                    genome[key] = random.randint(config['min'], config['max'])
                elif config['type'] == 'float':
                    genome[key] = random.uniform(config['min'], config['max'])
            
            fitness = self.evaluate(genome)
            
            if fitness > best_fitness:
                best_fitness = fitness
                best_genome = genome
                print(f"[{i+1}] New best: {fitness:.2f} <- {genome}")
        
        return best_genome, best_fitness
    
    def evaluate(self, genome):
        """评估"""
        agent = Agent(i=2, o=4)
        
        # 应用变异
        for p in agent.net.parameters():
            if random.random() < genome.get('mutation_rate', 0.2):
                p.data += torch.randn_like(p) * genome.get('mutation_scale', 0.3)
        
        total = 0
        for _ in range(self.episodes):
            game = self.game_class()
            steps = 0
            max_steps = genome.get('max_steps', 20)
            
            while steps < max_steps:
                state = game.st()
                x = torch.tensor(state).float().unsqueeze(0)
                with torch.no_grad():
                    action = agent(x).argmax().item()
                r = game.act(action)
                total += r
                steps += 1
                if r > 0:
                    break
        
        return total / self.episodes


# 快速测试
def quick_test():
    print("="*50)
    print("Quick Game Parameter Search")
    print("="*50)
    
    schema = {
        'mutation_rate': {'type': 'float', 'min': 0.1, 'max': 0.4},
        'mutation_scale': {'type': 'float', 'min': 0.2, 'max': 0.8},
        'max_steps': {'type': 'int', 'min': 15, 'max': 30}
    }
    
    print("\n[Maze]")
    opt = QuickOptimizer(Maze, schema, episodes=10)
    best, fitness = opt.random_search(iterations=10)
    print(f"Best: {best}, Score: {fitness:.2f}")
    
    print("\n[Predator]")
    opt = QuickOptimizer(Predator, schema, episodes=10)
    best, fitness = opt.random_search(iterations=10)
    print(f"Best: {best}, Score: {fitness:.2f}")


if __name__ == "__main__":
    quick_test()
