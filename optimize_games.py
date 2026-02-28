# -*- coding: utf-8 -*-
"""
Edge Swarm Game Optimizer - 边缘演化群游戏优化器
用演化算法优化游戏AI参数
"""

import random
import sys
import os
from typing import List, Dict, Callable

# 添加项目路径
sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace\edge_swarm_system")
from all_games_improved import *


class GameOptimizer:
    """游戏AI演化优化器"""
    
    def __init__(self, game_class, genome_schema: Dict, episodes: int = 50):
        self.game_class = game_class
        self.genome_schema = genome_schema
        self.episodes = episodes
        self.population: List[Dict] = []
        self.best_genome = None
        self.best_fitness = -float('inf')
        self.generation = 0
    
    def init_population(self, size: int = 20):
        """初始化种群"""
        for i in range(size):
            genome = {}
            for key, config in self.genome_schema.items():
                if config['type'] == 'int':
                    genome[key] = random.randint(config['min'], config['max'])
                elif config['type'] == 'float':
                    genome[key] = random.uniform(config['min'], config['max'])
            
            self.population.append({
                'genome': genome,
                'fitness': 0.0
            })
        
        print(f"[Init] {self.game_class.NAME}: {size} variants")
    
    def evaluate(self, genome: Dict) -> float:
        """评估单个基因"""
        # 创建智能体
        mutation_rate = genome.get('mutation_rate', 0.2)
        mutation_scale = genome.get('mutation_scale', 0.3)
        
        # 创建agent
        agent = Agent(i=2, o=4)
        
        # 训练和评估
        total_reward = 0
        
        for ep in range(self.episodes):
            game = self.game_class()
            steps = 0
            max_steps = genome.get('max_steps', 20)
            
            while steps < max_steps:
                state = game.st()
                x = torch.tensor(state).float().unsqueeze(0)
                
                with torch.no_grad():
                    action = agent(x).argmax().item()
                
                reward = game.act(action)
                total_reward += reward
                steps += 1
                
                if reward > 0:  # 成功
                    break
        
        return total_reward / self.episodes
    
    def evolve(self, generations: int = 20, population_size: int = 20):
        """运行演化"""
        self.init_population(population_size)
        
        for gen in range(generations):
            # 评估
            for variant in self.population:
                variant['fitness'] = self.evaluate(variant['genome'])
                
                if variant['fitness'] > self.best_fitness:
                    self.best_fitness = variant['fitness']
                    self.best_genome = variant['genome'].copy()
            
            # 选择精英
            sorted_pop = sorted(self.population, key=lambda x: x['fitness'], reverse=True)
            elite = sorted_pop[:max(2, len(sorted_pop) // 5)]
            
            # 生成新种群
            new_pop = list(elite)
            
            while len(new_pop) < population_size:
                parent = random.choice(elite)
                child = self._mutate(parent['genome'])
                new_pop.append({'genome': child, 'fitness': 0.0})
            
            self.population = new_pop
            self.generation += 1
            
            print(f"[Gen {gen+1}] Best: {self.best_fitness:.2f}, Current: {sorted_pop[0]['fitness']:.2f}")
        
        return self.best_genome, self.best_fitness
    
    def _mutate(self, genome: Dict) -> Dict:
        """变异"""
        new_genome = genome.copy()
        
        for key, config in self.genome_schema.items():
            if random.random() < 0.3:  # 30%变异率
                if config['type'] == 'int':
                    delta = random.randint(-config.get('step', 1), config.get('step', 1))
                    new_genome[key] = max(config['min'], min(config['max'], 
                        new_genome[key] + delta))
                elif config['type'] == 'float':
                    delta = random.uniform(-config.get('step', 0.05), config.get('step', 0.05))
                    new_genome[key] = max(config['min'], min(config['max'], 
                        new_genome[key] + delta))
        
        return new_genome


def optimize_maze():
    """优化迷宫游戏"""
    print("\n" + "="*50)
    print("Optimizing: Maze Game")
    print("="*50)
    
    schema = {
        'mutation_rate': {'type': 'float', 'min': 0.05, 'max': 0.5, 'step': 0.05},
        'mutation_scale': {'type': 'float', 'min': 0.1, 'max': 1.0, 'step': 0.1},
        'max_steps': {'type': 'int', 'min': 10, 'max': 50, 'step': 5}
    }
    
    optimizer = GameOptimizer(Maze, schema, episodes=30)
    best, fitness = optimizer.evolve(generations=15, population_size=15)
    
    print(f"\nBest genome: {best}")
    print(f"Best fitness: {fitness:.2f}")
    
    return best, fitness


def optimize_predator():
    """优化捕食者游戏"""
    print("\n" + "="*50)
    print("Optimizing: Predator Game")
    print("="*50)
    
    schema = {
        'mutation_rate': {'type': 'float', 'min': 0.05, 'max': 0.5, 'step': 0.05},
        'mutation_scale': {'type': 'float', 'min': 0.1, 'max': 1.0, 'step': 0.1},
        'max_steps': {'type': 'int', 'min': 20, 'max': 100, 'step': 10}
    }
    
    optimizer = GameOptimizer(Predator, schema, episodes=30)
    best, fitness = optimizer.evolve(generations=15, population_size=15)
    
    print(f"\nBest genome: {best}")
    print(f"Best fitness: {fitness:.2f}")
    
    return best, fitness


def optimize_survival():
    """优化生存游戏"""
    print("\n" + "="*50)
    print("Optimizing: Survival Game")
    print("="*50)
    
    schema = {
        'mutation_rate': {'type': 'float', 'min': 0.05, 'max': 0.5, 'step': 0.05},
        'mutation_scale': {'type': 'float', 'min': 0.1, 'max': 1.0, 'step': 0.1},
        'max_steps': {'type': 'int', 'min': 20, 'max': 100, 'step': 10}
    }
    
    optimizer = GameOptimizer(Survival, schema, episodes=30)
    best, fitness = optimizer.evolve(generations=15, population_size=15)
    
    print(f"\nBest genome: {best}")
    print(f"Best fitness: {fitness:.2f}")
    
    return best, fitness


if __name__ == "__main__":
    results = {}
    
    results['Maze'] = optimize_maze()
    results['Predator'] = optimize_predator()
    results['Survival'] = optimize_survival()
    
    print("\n" + "="*50)
    print("OPTIMIZATION COMPLETE")
    print("="*50)
    
    for game, (genome, fitness) in results.items():
        print(f"\n{game}:")
        print(f"  Fitness: {fitness:.2f}")
        print(f"  Parameters: {genome}")
