# -*- coding: utf-8 -*-
"""
Self-Optimizing Continuum - 自我优化系统
系统优化自己的参数
"""

import random
import time
from typing import List, Dict, Callable
from dataclasses import dataclass, field


# ==================== 可调参数 ====================

@dataclass
class MetaParameters:
    """元参数 - 系统可调参数"""
    # 仲裁者参数
    idle_threshold: float = 10.0  # 多少秒无任务转为漫游
    task_interrupt_threshold: int = 8  # 任务优先级阈值
    
    # 思维生成参数
    drift_temperature: float = 0.8  # 漫游态创造性
    focus_temperature: float = 0.3  # 专注态确定性
    integration_temperature: float = 0.5  # 整合态平衡
    
    # 记忆参数
    buffer_size: int = 20
    memory_retention_rate: float = 0.7  # 记忆保留率
    
    # 演化参数
    mutation_rate: float = 0.3
    elite_ratio: float = 0.2
    
    def to_dict(self) -> Dict:
        return {
            'idle_threshold': self.idle_threshold,
            'task_interrupt_threshold': self.task_interrupt_threshold,
            'drift_temperature': self.drift_temperature,
            'focus_temperature': self.focus_temperature,
            'integration_temperature': self.integration_temperature,
            'buffer_size': self.buffer_size,
            'memory_retention_rate': self.memory_retention_rate,
            'mutation_rate': self.mutation_rate,
            'elite_ratio': self.elite_ratio
        }


# ==================== 自我优化器 ====================

class SelfOptimizer:
    """自我优化器 - 优化系统参数"""
    
    def __init__(self):
        self.population: List[MetaParameters] = []
        self.best_params: MetaParameters = MetaParameters()
        self.best_fitness: float = -float('inf')
        self.generation = 0
        self.history: List[Dict] = []
    
    def init_population(self, size: int = 10):
        """初始化种群"""
        for _ in range(size):
            params = MetaParameters(
                idle_threshold=random.uniform(5, 20),
                task_interrupt_threshold=random.randint(5, 10),
                drift_temperature=random.uniform(0.5, 1.0),
                focus_temperature=random.uniform(0.1, 0.5),
                integration_temperature=random.uniform(0.3, 0.7),
                buffer_size=random.randint(10, 30),
                memory_retention_rate=random.uniform(0.5, 0.9),
                mutation_rate=random.uniform(0.1, 0.5),
                elite_ratio=random.uniform(0.1, 0.3)
            )
            self.population.append(params)
        
        print(f"[Init] Created {size} parameter variants")
    
    def evaluate(self, params: MetaParameters) -> float:
        """评估参数 - 模拟系统运行"""
        
        # 模拟系统行为
        score = 0.0
        
        # 1. 响应速度 (idle_threshold 越低越好)
        score += (20 - params.idle_threshold) / 20 * 0.2
        
        # 2. 任务处理 (task_interrupt_threshold 适中最好)
        score += (1 - abs(params.task_interrupt_threshold - 7) / 5) * 0.2
        
        # 3. 创造性 (drift_temperature 越高越好)
        score += params.drift_temperature * 0.15
        
        # 4. 专注力 (focus_temperature 越低越好)
        score += (1 - params.focus_temperature) * 0.15
        
        # 5. 平衡性 (integration_temperature 适中)
        score += (1 - abs(params.integration_temperature - 0.5) * 2) * 0.1
        
        # 6. 记忆效率
        score += params.memory_retention_rate * 0.1
        
        # 7. 演化效率
        score += (1 - params.mutation_rate) * 0.05
        score += params.elite_ratio * 0.05
        
        # 添加随机波动
        score += random.uniform(-0.1, 0.1)
        
        return max(0, min(1, score))
    
    def evolve(self, generations: int = 20):
        """演化优化"""
        self.init_population(size=10)
        
        for gen in range(generations):
            # 评估
            for params in self.population:
                fitness = self.evaluate(params)
                
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_params = params
            
            # 选择精英
            sorted_pop = sorted(self.population, 
                             key=lambda p: self.evaluate(p), 
                             reverse=True)
            elite = sorted_pop[:max(2, len(sorted_pop) // 5)]
            
            # 生成新种群
            new_pop = list(elite)
            
            while len(new_pop) < len(self.population):
                parent = random.choice(elite)
                child = self._mutate(parent)
                new_pop.append(child)
            
            self.population = new_pop
            self.generation += 1
            
            current_best = self.evaluate(sorted_pop[0])
            print(f"[Gen {gen+1}] Best: {current_best:.3f}, Overall Best: {self.best_fitness:.3f}")
            
            self.history.append({
                'generation': gen + 1,
                'best_fitness': current_best,
                'overall_best': self.best_fitness,
                'best_params': sorted_pop[0].to_dict()
            })
        
        return self.best_params, self.best_fitness
    
    def _mutate(self, parent: MetaParameters) -> MetaParameters:
        """变异参数"""
        return MetaParameters(
            idle_threshold=max(1, min(30, 
                parent.idle_threshold + random.uniform(-2, 2))),
            task_interrupt_threshold=max(1, min(10, 
                parent.task_interrupt_threshold + random.randint(-1, 1))),
            drift_temperature=max(0.1, min(1.0, 
                parent.drift_temperature + random.uniform(-0.1, 0.1))),
            focus_temperature=max(0.0, min(0.9, 
                parent.focus_temperature + random.uniform(-0.1, 0.1))),
            integration_temperature=max(0.1, min(0.9, 
                parent.integration_temperature + random.uniform(-0.1, 0.1))),
            buffer_size=max(5, min(50, 
                parent.buffer_size + random.randint(-3, 3))),
            memory_retention_rate=max(0.1, min(1.0, 
                parent.memory_retention_rate + random.uniform(-0.1, 0.1))),
            mutation_rate=max(0.05, min(0.8, 
                parent.mutation_rate + random.uniform(-0.1, 0.1))),
            elite_ratio=max(0.05, min(0.5, 
                parent.elite_ratio + random.uniform(-0.05, 0.05)))
        )


# ==================== 自我优化演示 ====================

def demo_self_optimization():
    """演示自我优化"""
    print("\n" + "="*60)
    print("Self-Optimizing Continuum Demo")
    print("="*60)
    
    optimizer = SelfOptimizer()
    best_params, best_fitness = optimizer.evolve(generations=20)
    
    print("\n" + "="*60)
    print("Optimization Complete!")
    print("="*60)
    
    print(f"\nBest Fitness: {best_fitness:.3f}")
    print("\nBest Parameters:")
    for key, value in best_params.to_dict().items():
        print(f"  {key}: {value:.3f}")
    
    return best_params


# ==================== 元学习循环 ====================

class MetaLearningLoop:
    """元学习循环 - 持续自我优化"""
    
    def __init__(self):
        self.optimizer = SelfOptimizer()
        self.current_params = MetaParameters()
        self.iteration = 0
    
    def run(self, iterations: int = 5):
        """运行多轮自我优化"""
        
        print("\n" + "="*60)
        print("Meta-Learning Loop: Self-Improving System")
        print("="*60)
        
        for i in range(iterations):
            self.iteration += 1
            
            print(f"\n--- Iteration {self.iteration} ---")
            print(f"Current Params: {self.current_params.to_dict()}")
            
            # 用当前参数运行系统
            fitness = self._run_with_params(self.current_params)
            print(f"Performance: {fitness:.3f}")
            
            # 优化参数
            best_params, best_fitness = self.optimizer.evolve(generations=10)
            
            # 更新参数
            self.current_params = best_params
            print(f"Updated to: {best_params.to_dict()}")
        
        print("\n" + "="*60)
        print("Final Optimized Parameters:")
        print("="*60)
        for key, value in self.current_params.to_dict().items():
            print(f"  {key}: {value:.3f}")
    
    def _run_with_params(self, params: MetaParameters) -> float:
        """用指定参数运行系统 - 模拟"""
        # 模拟系统运行
        score = 0.5
        
        # 参数影响得分
        score += (params.drift_temperature - 0.5) * 0.2
        score += (0.5 - params.focus_temperature) * 0.2
        score += params.memory_retention_rate * 0.1
        
        return max(0, min(1, score + random.uniform(-0.1, 0.1)))


if __name__ == "__main__":
    # 简单演示
    demo_self_optimization()
    
    # 元学习演示
    # meta = MetaLearningLoop()
    # meta.run(iterations=3)
