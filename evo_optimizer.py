# -*- coding: utf-8 -*-
"""
Evolutionary Optimizer - 通用演化优化器
可以用它来优化任何项目的参数
"""

import random
from typing import List, Dict, Callable


class EvolutionOptimizer:
    """通用演化优化器"""
    
    def __init__(self, 
                 genome_schema: Dict,
                 fitness_fn: Callable,
                 population_size: int = 10,
                 mutation_rate: float = 0.3):
        
        self.genome_schema = genome_schema  # 基因定义
        self.fitness_fn = fitness_fn          # 适应度函数
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        
        self.population: List[Dict] = []
        self.generation = 0
        self.best_solution = None
        self.best_fitness = -float('inf')
    
    def init_population(self):
        """初始化种群"""
        for i in range(self.population_size):
            genome = {}
            for key, config in self.genome_schema.items():
                if config['type'] == 'int':
                    genome[key] = random.randint(config['min'], config['max'])
                elif config['type'] == 'float':
                    genome[key] = random.uniform(config['min'], config['max'])
                elif config['type'] == 'choice':
                    genome[key] = random.choice(config['options'])
            
            self.population.append({
                'genome': genome,
                'fitness': 0.0
            })
        
        print(f"[Init] Created {len(self.population)} variants")
    
    def evolve_one_generation(self):
        """演化一代"""
        # 评估适应度
        for variant in self.population:
            variant['fitness'] = self.fitness_fn(variant['genome'])
            
            if variant['fitness'] > self.best_fitness:
                self.best_fitness = variant['fitness']
                self.best_solution = variant['genome'].copy()
        
        # 选择精英
        sorted_pop = sorted(self.population, key=lambda x: x['fitness'], reverse=True)
        elite = sorted_pop[:max(2, len(sorted_pop) // 5)]
        
        # 生成新种群
        new_pop = list(elite)
        
        while len(new_pop) < self.population_size:
            parent = random.choice(elite)
            child = self._mutate(parent['genome'])
            new_pop.append({'genome': child, 'fitness': 0.0})
        
        self.population = new_pop
        self.generation += 1
        
        return self.best_fitness
    
    def _mutate(self, genome: Dict) -> Dict:
        """变异"""
        new_genome = genome.copy()
        
        for key, config in self.genome_schema.items():
            if random.random() < self.mutation_rate:
                if config['type'] == 'int':
                    delta = random.randint(-config.get('step', 1), config.get('step', 1))
                    new_genome[key] = max(config['min'], min(config['max'], 
                        new_genome[key] + delta))
                elif config['type'] == 'float':
                    delta = random.uniform(-config.get('step', 0.1), config.get('step', 0.1))
                    new_genome[key] = max(config['min'], min(config['max'], 
                        new_genome[key] + delta))
                elif config['type'] == 'choice':
                    new_genome[key] = random.choice(config['options'])
        
        return new_genome
    
    def run(self, generations: int = 10) -> Dict:
        """运行演化"""
        self.init_population()
        
        for gen in range(generations):
            fitness = self.evolve_one_generation()
            print(f"[Gen {gen+1}] Best fitness: {fitness:.4f}")
        
        return {
            'best_genome': self.best_solution,
            'best_fitness': self.best_fitness,
            'generations': self.generation
        }


# ==================== 示例1: 优化游戏参数 ====================

def game_fitness(genome: Dict) -> float:
    """游戏适应度函数"""
    speed = genome['speed']
    aggression = genome['aggression']
    defense = genome['defense']
    
    # 模拟游戏得分
    score = (speed * 0.3 + aggression * 0.4 + defense * 0.3)
    
    # 平衡性惩罚 - 不能太极端
    balance_penalty = abs(speed - 50) / 50 * 0.2
    balance_penalty += abs(aggression - 50) / 50 * 0.2
    
    return score - balance_penalty


def optimize_game():
    """优化游戏参数"""
    print("\n" + "="*50)
    print("Example 1: Optimize Game Parameters")
    print("="*50)
    
    schema = {
        'speed': {'type': 'int', 'min': 1, 'max': 100, 'step': 5},
        'aggression': {'type': 'int', 'min': 1, 'max': 100, 'step': 5},
        'defense': {'type': 'int', 'min': 1, 'max': 100, 'step': 5}
    }
    
    optimizer = EvolutionOptimizer(
        genome_schema=schema,
        fitness_fn=game_fitness,
        population_size=20,
        mutation_rate=0.4
    )
    
    result = optimizer.run(generations=20)
    
    print(f"\nBest game params: {result['best_genome']}")
    print(f"Best fitness: {result['best_fitness']:.4f}")


# ==================== 示例2: 优化Prompt ====================

def prompt_fitness(genome: Dict) -> float:
    """Prompt适应度函数"""
    length = genome['length']
    style = genome['style']
    
    # 模拟评估
    score = 0.5
    
    if length == 'short':
        score += 0.3
    elif length == 'medium':
        score += 0.2
    
    if style == 'direct':
        score += 0.3
    elif style == 'friendly':
        score += 0.2
    
    return score + random.uniform(-0.1, 0.1)


def optimize_prompt():
    """优化Prompt"""
    print("\n" + "="*50)
    print("Example 2: Optimize Prompt")
    print("="*50)
    
    schema = {
        'length': {'type': 'choice', 'options': ['short', 'medium', 'long']},
        'style': {'type': 'choice', 'options': ['direct', 'friendly', 'formal']},
        'temperature': {'type': 'float', 'min': 0.0, 'max': 1.0, 'step': 0.1}
    }
    
    optimizer = EvolutionOptimizer(
        genome_schema=schema,
        fitness_fn=prompt_fitness,
        population_size=15,
        mutation_rate=0.3
    )
    
    result = optimizer.run(generations=15)
    
    print(f"\nBest prompt: {result['best_genome']}")
    print(f"Best fitness: {result['best_fitness']:.4f}")


# ==================== 示例3: 优化神经网络超参数 ====================

def nn_fitness(genome: Dict) -> float:
    """神经网络适应度"""
    lr = genome['learning_rate']
    batch = genome['batch_size']
    layers = genome['layers']
    
    # 模拟训练结果
    score = 0.7
    
    # 学习率影响
    if 0.001 <= lr <= 0.01:
        score += 0.2
    
    # batch影响
    if 32 <= batch <= 128:
        score += 0.1
    
    return score + random.uniform(-0.05, 0.05)


def optimize_nn():
    """优化神经网络"""
    print("\n" + "="*50)
    print("Example 3: Optimize Neural Network")
    print("="*50)
    
    schema = {
        'learning_rate': {'type': 'float', 'min': 0.0001, 'max': 0.1, 'step': 0.001},
        'batch_size': {'type': 'choice', 'options': [16, 32, 64, 128, 256]},
        'layers': {'type': 'int', 'min': 1, 'max': 10, 'step': 1},
        'dropout': {'type': 'float', 'min': 0.0, 'max': 0.5, 'step': 0.1}
    }
    
    optimizer = EvolutionOptimizer(
        genome_schema=schema,
        fitness_fn=nn_fitness,
        population_size=20,
        mutation_rate=0.3
    )
    
    result = optimizer.run(generations=25)
    
    print(f"\nBest NN params: {result['best_genome']}")
    print(f"Best fitness: {result['best_fitness']:.4f}")


if __name__ == "__main__":
    optimize_game()
    optimize_prompt()
    optimize_nn()
