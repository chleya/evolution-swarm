# -*- coding: utf-8 -*-
"""
Evolutionary Swarm - Main Entry Point
演化智能群 - 主入口
"""

import argparse
import random
from typing import List, Dict, Optional


class EvolutionarySwarm:
    """演化智能群主类"""
    
    def __init__(self, 
                 population_size: int = 10,
                 mutation_rate: float = 0.3,
                 crossover_rate: float = 0.5):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        self.population: List[Dict] = []
        self.tasks: List[Dict] = []
        self.generation = 0
        
        # 思维模式
        self.modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
        
        # 初始化种群
        self._init_population()
    
    def _init_population(self):
        """初始化种群"""
        for i in range(self.population_size):
            variant = {
                'id': f'agent_{i}',
                'generation': 0,
                'mode': random.choice(self.modes),
                'depth': random.randint(3, 8),
                'fitness': 0.0,
                'tasks_completed': 0,
                'successes': 0
            }
            self.population.append(variant)
        
        print(f"[Init] Created {len(self.population)} agents")
    
    def add_task(self, task_id: str, task_prompt: str, priority: int = 5, task_type: str = "general"):
        """添加任务"""
        self.tasks.append({
            'id': task_id,
            'prompt': task_prompt,
            'priority': priority,
            'type': task_type,
            'status': 'pending'
        })
    
    def run_once(self) -> Dict:
        """运行一代"""
        self.generation += 1
        
        # 每个agent执行多个任务
        tasks_per_agent = 3
        for agent in self.population:
            for _ in range(tasks_per_agent):
                if self.tasks:
                    task = random.choice(self.tasks)
                    self._execute_task(agent, task)
        
        # 评估适应度
        self._evaluate()
        
        # 演化
        self._evolve()
        
        return self.get_status()
    
    def _select_agent(self) -> Dict:
        """选择最佳agent"""
        # 简单选择：适应度最高的
        return max(self.population, key=lambda x: x['fitness'])
    
    def _execute_task(self, agent: Dict, task: Dict) -> bool:
        """执行任务 - 模拟"""
        # 模拟执行 - 加入随机性
        mode = agent['mode']
        depth = agent['depth']
        
        # 不同思维模式适合不同任务
        task_type = task.get('type', 'general')
        
        # 模式匹配矩阵
        mode_bonus = {
            ('math', 'analytical'): 0.25,
            ('math', 'critical'): 0.20,
            ('logic', 'critical'): 0.25,
            ('logic', 'systematic'): 0.20,
            ('puzzle', 'creative'): 0.25,
            ('puzzle', 'intuitive'): 0.20,
            ('algorithm', 'systematic'): 0.25,
            ('algorithm', 'analytical'): 0.20,
        }
        
        # 基础正确率
        rate = 0.3
        
        # 模式加成
        key = (task_type, mode)
        rate += mode_bonus.get(key, 0)
        
        # 深度加成/惩罚
        if depth >= 5:
            rate += 0.10
        elif depth < 3:
            rate -= 0.10
        
        # 添加随机波动
        rate += random.uniform(-0.1, 0.1)
        
        # 限制范围
        rate = max(0.1, min(0.9, rate))
        
        success = random.random() < rate
        
        # 更新统计
        agent['tasks_completed'] += 1
        if success:
            agent['successes'] += 1
        
        return success
    
    def _evaluate(self):
        """评估适应度"""
        for agent in self.population:
            if agent['tasks_completed'] > 0:
                agent['fitness'] = agent['successes'] / agent['tasks_completed']
            else:
                agent['fitness'] = 0.0
    
    def _evolve(self):
        """演化下一代"""
        # 排序
        sorted_pop = sorted(self.population, key=lambda x: x['fitness'], reverse=True)
        
        # 精英保留
        elite_count = max(2, self.population_size // 5)
        elite = sorted_pop[:elite_count]
        
        # 生成新种群
        new_pop = list(elite)
        
        while len(new_pop) < self.population_size:
            # 变异或交叉
            if random.random() < self.crossover_rate:
                # 交叉
                p1, p2 = random.sample(elite, 2)
                child = self._crossover(p1, p2)
            else:
                # 变异
                parent = random.choice(elite)
                child = self._mutate(parent)
            
            new_pop.append(child)
        
        self.population = new_pop
    
    def _mutate(self, parent: Dict) -> Dict:
        """变异"""
        child = parent.copy()
        child['id'] = f"agent_{random.randint(1000, 9999)}"
        child['generation'] = parent['generation'] + 1
        child['tasks_completed'] = 0
        child['successes'] = 0
        child['fitness'] = 0.0
        
        # 变异思维模式
        if random.random() < self.mutation_rate:
            child['mode'] = random.choice(self.modes)
        
        # 变异深度
        if random.random() < self.mutation_rate:
            child['depth'] = max(1, min(10, child['depth'] + random.randint(-1, 1)))
        
        return child
    
    def _crossover(self, p1: Dict, p2: Dict) -> Dict:
        """交叉"""
        child = {
            'id': f"agent_{random.randint(1000, 9999)}",
            'generation': max(p1['generation'], p2['generation']) + 1,
            'mode': p1['mode'] if random.random() < 0.5 else p2['mode'],
            'depth': (p1['depth'] + p2['depth']) // 2,
            'fitness': 0.0,
            'tasks_completed': 0,
            'successes': 0
        }
        return child
    
    def get_status(self) -> Dict:
        """获取状态"""
        fitness_values = [a['fitness'] for a in self.population]
        
        best = max(self.population, key=lambda x: x['fitness'])
        
        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'avg_fitness': sum(fitness_values) / len(fitness_values) if fitness_values else 0,
            'best_fitness': max(fitness_values) if fitness_values else 0,
            'best_mode': best['mode'],
            'best_depth': best['depth'],
            'tasks_completed': sum(a['tasks_completed'] for a in self.population)
        }
    
    def run(self, generations: int = 10):
        """运行多代"""
        print(f"\n{'='*60}")
        print(f"Evolutionary Swarm - Starting {generations} generations")
        print(f"{'='*60}\n")
        
        for gen in range(generations):
            self.run_once()
            
            status = self.get_status()
            print(f"[Gen {status['generation']}] "
                  f"Avg: {status['avg_fitness']:.1%}, "
                  f"Best: {status['best_fitness']:.1%} "
                  f"({status['best_mode']}, depth={status['best_depth']})")
        
        print(f"\n{'='*60}")
        print("Final Results:")
        print(self.get_status())
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description='Evolutionary Swarm')
    parser.add_argument('--generations', type=int, default=10, help='Number of generations')
    parser.add_argument('--population', type=int, default=10, help='Population size')
    parser.add_argument('--problems', type=int, default=3, help='Problems per generation')
    parser.add_argument('--mutation-rate', type=float, default=0.3, help='Mutation rate')
    parser.add_argument('--mode', type=str, default='random', help='指定思维模式')
    parser.add_argument('--demo', action='store_true', help='Run demo')
    
    args = parser.parse_args()
    
    # 创建系统
    swarm = EvolutionarySwarm(
        population_size=args.population,
        mutation_rate=args.mutation_rate
    )
    
    # 添加任务 (带类型)
    tasks = [
        ("math_1", "求解: 2x + 5 = 15", "math"),
        ("math_2", "求解: x^2 - 4 = 0", "math"),
        ("logic_1", "如果A>B, B>C, 则A>C?", "logic"),
        ("puzzle_1", "100个球，1个重，最少称几次?", "puzzle"),
        ("algorithm_1", "如何在排序数组中快速查找?", "algorithm")
    ]
    
    for task_id, prompt, task_type in tasks[:args.problems]:
        swarm.add_task(task_id, prompt, task_type=task_type)
    
    # 运行
    if args.demo:
        # 交互演示
        print("\n[Demo Mode]")
        for i in range(3):
            print(f"\n--- Round {i+1} ---")
            swarm.run_once()
            status = swarm.get_status()
            print(f"Status: {status}")
    else:
        # 批量运行
        swarm.run(generations=args.generations)


if __name__ == "__main__":
    main()
