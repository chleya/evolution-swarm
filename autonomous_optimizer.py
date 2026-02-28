# -*- coding: utf-8 -*-
"""
Autonomous Multi-Direction Optimizer - 自主多方向探索优化
不需要指令，自己探索不同方向
"""

import random
import time
from typing import List, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OptimizationDirection:
    """优化方向"""
    id: str
    name: str
    description: str
    target_params: Dict  # 要优化的参数
    fitness_fn: Callable  # 评估函数
    weight: float = 1.0  # 方向权重


@dataclass
class ExplorationResult:
    """探索结果"""
    direction_id: str
    generation: int
    best_fitness: float
    best_params: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AutonomousOptimizer:
    """自主多方向优化器"""
    
    def __init__(self):
        self.directions: List[OptimizationDirection] = []
        self.populations: Dict[str, List] = {}  # 每个方向一个种群
        self.results: List[ExplorationResult] = []
        self.is_running = False
        self.current_iteration = 0
        
        # 注册优化方向
        self._register_directions()
    
    def _register_directions(self):
        """注册优化方向"""
        
        # 方向1: 速度优先
        self.directions.append(OptimizationDirection(
            id="speed",
            name="Speed Optimizer",
            description="Optimize for speed and responsiveness",
            target_params={
                'idle_threshold': (1, 10),
                'task_interrupt_threshold': (1, 5),
                'focus_temperature': (0.0, 0.3)
            },
            fitness_fn=lambda p: self._eval_speed(p)
        ))
        
        # 方向2: 创造性优先
        self.directions.append(OptimizationDirection(
            id="creative",
            name="Creative Optimizer",
            description="Optimize for creativity and novelty",
            target_params={
                'drift_temperature': (0.6, 1.0),
                'memory_retention_rate': (0.3, 0.6)
            },
            fitness_fn=lambda p: self._eval_creative(p)
        ))
        
        # 方向3: 稳定性优先
        self.directions.append(OptimizationDirection(
            id="stable",
            name="Stable Optimizer",
            description="Optimize for stability and consistency",
            target_params={
                'mutation_rate': (0.05, 0.2),
                'elite_ratio': (0.3, 0.5),
                'buffer_size': (20, 40)
            },
            fitness_fn=lambda p: self._eval_stable(p)
        ))
        
        # 方向4: 效率优先
        self.directions.append(OptimizationDirection(
            id="efficiency",
            name="Efficiency Optimizer",
            description="Optimize for resource efficiency",
            target_params={
                'buffer_size': (5, 15),
                'memory_retention_rate': (0.1, 0.4)
            },
            fitness_fn=lambda p: self._eval_efficiency(p)
        ))
        
        # 方向5: 平衡优先
        self.directions.append(OptimizationDirection(
            id="balanced",
            name="Balanced Optimizer",
            description="Optimize for overall balance",
            target_params={
                'drift_temperature': (0.4, 0.6),
                'focus_temperature': (0.2, 0.4),
                'integration_temperature': (0.4, 0.6)
            },
            fitness_fn=lambda p: self._eval_balanced(p)
        ))
        
        print(f"[Init] Registered {len(self.directions)} optimization directions")
    
    # 评估函数
    def _eval_speed(self, p: Dict) -> float:
        score = 0
        score += (10 - p.get('idle_threshold', 10)) / 10 * 0.4
        score += (5 - p.get('task_interrupt_threshold', 5)) / 5 * 0.3
        score += (0.3 - p.get('focus_temperature', 0.3)) / 0.3 * 0.3
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))
    
    def _eval_creative(self, p: Dict) -> float:
        score = 0
        score += (p.get('drift_temperature', 0.5) - 0.4) / 0.6 * 0.5
        score += (0.6 - p.get('memory_retention_rate', 0.5)) / 0.6 * 0.3
        score += random.uniform(0.2, 0.3)
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))
    
    def _eval_stable(self, p: Dict) -> float:
        score = 0
        score += (0.2 - p.get('mutation_rate', 0.2)) / 0.2 * 0.3
        score += (p.get('elite_ratio', 0.3) - 0.2) / 0.3 * 0.3
        score += (p.get('buffer_size', 20) - 10) / 30 * 0.2
        score += random.uniform(0.2, 0.3)
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))
    
    def _eval_efficiency(self, p: Dict) -> float:
        score = 0
        score += (15 - p.get('buffer_size', 15)) / 15 * 0.4
        score += (0.4 - p.get('memory_retention_rate', 0.4)) / 0.4 * 0.4
        score += random.uniform(0.2, 0.3)
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))
    
    def _eval_balanced(self, p: Dict) -> float:
        score = 0.5
        # 接近0.5的平衡点
        score -= abs(p.get('drift_temperature', 0.5) - 0.5) * 0.5
        score -= abs(p.get('focus_temperature', 0.3) - 0.3) * 0.5
        score -= abs(p.get('integration_temperature', 0.5) - 0.5) * 0.3
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))
    
    def init_population(self, direction: OptimizationDirection, size: int = 10):
        """初始化种群"""
        pop = []
        for _ in range(size):
            genome = {}
            for param, (min_val, max_val) in direction.target_params.items():
                if isinstance(min_val, int):
                    genome[param] = random.randint(min_val, max_val)
                else:
                    genome[param] = random.uniform(min_val, max_val)
            pop.append({'genome': genome, 'fitness': 0.0})
        
        self.populations[direction.id] = pop
    
    def evolve_one_step(self, direction_id: str) -> ExplorationResult:
        """演化一步"""
        direction = next(d for d in self.directions if d.id == direction_id)
        pop = self.populations[direction_id]
        
        # 评估
        for variant in pop:
            variant['fitness'] = direction.fitness_fn(variant['genome'])
        
        # 选择精英
        sorted_pop = sorted(pop, key=lambda x: x['fitness'], reverse=True)
        elite = sorted_pop[:max(2, len(sorted_pop) // 3)]
        
        # 生成新个体
        new_pop = list(elite)
        while len(new_pop) < len(pop):
            parent = random.choice(elite)
            child = self._mutate(parent['genome'], direction.target_params)
            new_pop.append({'genome': child, 'fitness': 0.0})
        
        self.populations[direction_id] = new_pop
        
        # 记录最佳
        best = sorted_pop[0]
        result = ExplorationResult(
            direction_id=direction_id,
            generation=self.current_iteration,
            best_fitness=best['fitness'],
            best_params=best['genome']
        )
        self.results.append(result)
        
        return result
    
    def _mutate(self, genome: Dict, target_params: Dict) -> Dict:
        """变异"""
        new_genome = genome.copy()
        for param, (min_val, max_val) in target_params.items():
            if random.random() < 0.3:
                if isinstance(min_val, int):
                    delta = random.randint(-2, 2)
                    new_genome[param] = max(min_val, min(max_val, new_genome[param] + delta))
                else:
                    delta = random.uniform(-0.1, 0.1)
                    new_genome[param] = max(min_val, min(max_val, new_genome[param] + delta))
        return new_genome
    
    def run_autonomously(self, steps_per_direction: int = 10):
        """自主运行 - 多方向同时探索"""
        self.is_running = True
        
        # 初始化所有方向的种群
        for direction in self.directions:
            self.init_population(direction, size=10)
        
        print("\n" + "="*70)
        print("AUTONOMOUS MULTI-DIRECTION OPTIMIZATION")
        print("="*70)
        
        iteration = 0
        while self.is_running and iteration < steps_per_direction:
            iteration += 1
            self.current_iteration = iteration
            
            print(f"\n--- Iteration {iteration} ---")
            
            # 每个方向都演化一步
            for direction in self.directions:
                result = self.evolve_one_step(direction.id)
                
                direction_icon = {
                    'speed': '[SPEED]',
                    'creative': '[CREATIVE]',
                    'stable': '[STABLE]',
                    'efficiency': '[EFFICIENCY]',
                    'balanced': '[BALANCED]'
                }
                
                icon = direction_icon.get(direction.id, '[?]')
                print(f"{icon} {direction.name:20} | Fitness: {result.best_fitness:.3f}")
            
            # 等待
            time.sleep(0.2)
            
            # 检查是否需要重置方向
            if iteration % 20 == 0:
                self._explore_new_direction()
        
        print("\n" + "="*70)
        print("OPTIMIZATION COMPLETE")
        print("="*70)
        
        return self.get_summary()
    
    def _explore_new_direction(self):
        """探索新方向 - 随机变异"""
        # 随机选择一个方向重置
        direction = random.choice(self.directions)
        self.init_population(direction, size=10)
        print(f"\n>>> Exploring new direction: {direction.name}")
    
    def get_summary(self) -> Dict:
        """获取总结"""
        summary = {}
        
        for direction in self.directions:
            results = [r for r in self.results if r.direction_id == direction.id]
            if results:
                best = max(results, key=lambda x: x.best_fitness)
                summary[direction.id] = {
                    'name': direction.name,
                    'description': direction.description,
                    'best_fitness': best.best_fitness,
                    'best_params': best.best_params
                }
        
        return summary


# ==================== 演示 ====================

def demo():
    """演示"""
    print("\n" + "="*70)
    print("AUTONOMOUS OPTIMIZER - Self-Exploring System")
    print("="*70)
    
    optimizer = AutonomousOptimizer()
    
    # 自主运行
    summary = optimizer.run_autonomously(steps_per_direction=15)
    
    # 打印总结
    print("\n" + "="*70)
    print("RESULTS BY DIRECTION")
    print("="*70)
    
    for dir_id, data in summary.items():
        print(f"\n[{dir_id.upper()}] {data['name']}")
        print(f"  Description: {data['description']}")
        print(f"  Best Fitness: {data['best_fitness']:.3f}")
        print(f"  Best Params:")
        for param, value in data['best_params'].items():
            print(f"    - {param}: {value:.3f}")
    
    # 找出最佳方向
    best_direction = max(summary.items(), key=lambda x: x[1]['best_fitness'])
    print(f"\n{'='*70}")
    print(f"BEST DIRECTION: {best_direction[1]['name']} ({best_direction[1]['best_fitness']:.3f})")
    print(f"{'='*70}")


if __name__ == "__main__":
    demo()
