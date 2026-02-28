# -*- coding: utf-8 -*-
"""
Adaptive Population - 适应性种群
像生物一样适应环境，而不是优化数学函数
"""

import random
from typing import List, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Species:
    """物种 - 不同的生存策略"""
    id: str
    name: str
    strategy: Dict  # 策略参数
    fitness: float = 0.0
    alive: bool = True
    age: int = 0
    children: int = 0
    history: List[Dict] = field(default_factory=list)


@dataclass
class Environment:
    """环境 - 压力源"""
    name: str
    pressure_type: str  # what kind of pressure
    difficulty: float
    duration: int  # how long this environment lasts


class AdaptivePopulation:
    """适应性种群 - 像生物一样进化"""
    
    def __init__(self, population_size: int = 20):
        self.population: List[Species] = []
        self.population_size = population_size
        self.generation = 0
        self.environment_history: List[Dict] = []
        
        # 初始化物种多样性
        self._init_diversity()
    
    def _init_diversity(self):
        """初始化多样性 - 不同的生存策略"""
        
        strategies = [
            # 快速反应型
            {'name': 'Sprinter', 'speed': 0.9, 'caution': 0.2, 'energy': 0.5, 'social': 0.3},
            # 谨慎型
            {'name': 'Thinker', 'speed': 0.4, 'caution': 0.9, 'energy': 0.6, 'social': 0.5},
            # 社交型
            {'name': 'Socialite', 'speed': 0.5, 'caution': 0.5, 'energy': 0.5, 'social': 0.9},
            # 节能型
            {'name': 'Survivor', 'speed': 0.3, 'caution': 0.6, 'energy': 0.9, 'social': 0.3},
            # 激进型
            {'name': 'Hunter', 'speed': 0.8, 'caution': 0.3, 'energy': 0.7, 'social': 0.4},
            # 平衡型
            {'name': 'Balanced', 'speed': 0.5, 'caution': 0.5, 'energy': 0.5, 'social': 0.5},
        ]
        
        for i in range(self.population_size):
            strategy = random.choice(strategies).copy()
            species = Species(
                id=f"species_{i}",
                name=strategy['name'],
                strategy=strategy,
                fitness=1.0  # 初始适应性
            )
            self.population.append(species)
        
        print(f"[Init] Created {self.population_size} species with diverse strategies")
    
    def set_environment(self, env: Environment):
        """设置环境压力"""
        self.current_env = env
        self.environment_history.append({
            'generation': self.generation,
            'name': env.name,
            'pressure': env.pressure_type,
            'difficulty': env.difficulty
        })
        print(f"\n[Environment] {env.name} - {env.pressure_type} (difficulty: {env.difficulty})")
    
    def survive(self) -> List[Species]:
        """生存挑战 - 环境选择"""
        survivors = []
        
        for species in self.population:
            if not species.alive:
                continue
            
            # 计算生存概率
            survival_chance = self._calculate_survival(species, self.current_env)
            
            # 随机决定是否存活
            if random.random() < survival_chance:
                species.fitness += 0.1  # 适应增加
                species.age += 1
                survivors.append(species)
            else:
                species.alive = False
                species.fitness -= 0.2
        
        return survivors
    
    def _calculate_survival(self, species: Species, env: Environment) -> float:
        """计算生存概率 - 策略与环境匹配"""
        s = species.strategy
        e = env
        
        # 不同环境类型需要不同策略
        if e.pressure_type == 'speed':
            # 需要快速反应
            required = s['speed']
            match = required * (1 + random.uniform(-0.2, 0.2))
            survival = match * (1 - e.difficulty * 0.5)
        
        elif e.pressure_type == 'caution':
            # 需要谨慎
            required = s['caution']
            match = required * (1 + random.uniform(-0.2, 0.2))
            survival = match * (1 - e.difficulty * 0.5)
        
        elif e.pressure_type == 'energy':
            # 需要节能
            required = 1 - s['energy']  # 低能耗更好
            match = required * (1 + random.uniform(-0.2, 0.2))
            survival = match * (1 - e.difficulty * 0.5)
        
        elif e.pressure_type == 'social':
            # 需要社交合作
            required = s['social']
            match = required * (1 + random.uniform(-0.2, 0.2))
            survival = match * (1 - e.difficulty * 0.5)
        
        elif e.pressure_type == 'chaos':
            # 混乱环境 - 适者生存
            survival = 0.3 + s['speed'] * 0.3 + s['caution'] * 0.2
            survival *= (1 - e.difficulty * 0.5)
        
        else:
            survival = 0.5
        
        return max(0.1, min(0.95, survival))
    
    def reproduce(self, survivors: List[Species]):
        """繁殖 - 适者生存"""
        if not survivors:
            print("[Extinction] All species died!")
            return
        
        # 计算总适应度
        total_fitness = sum(s.fitness for s in survivors)
        
        new_population = []
        
        # 精英保留
        survivors.sort(key=lambda s: s.fitness, reverse=True)
        elite_count = max(2, len(survivors) // 3)
        
        for i, species in enumerate(survivors[:elite_count]):
            # 精英保留
            new_species = Species(
                id=f"gen{self.generation}_{i}",
                name=species.name,
                strategy=species.strategy.copy(),
                fitness=species.fitness
            )
            new_population.append(new_species)
            
            # 繁殖
            num_children = max(1, int(species.fitness / 2))
            for _ in range(num_children):
                if len(new_population) >= self.population_size:
                    break
                
                child = self._reproduce(species, survivors)
                new_population.append(child)
        
        # 填充到目标大小
        while len(new_population) < self.population_size:
            parent = random.choice(survivors)
            child = self._reproduce(parent, survivors)
            new_population.append(child)
        
        self.population = new_population[:self.population_size]
        self.generation += 1
    
    def _reproduce(self, parent: Species, pool: List[Species]) -> Species:
        """繁殖 - 变异和遗传"""
        
        # 变异
        child_strategy = parent.strategy.copy()
        
        # 随机变异
        if random.random() < 0.3:
            trait = random.choice(['speed', 'caution', 'energy', 'social'])
            child_strategy[trait] = max(0, min(1, 
                child_strategy[trait] + random.uniform(-0.2, 0.2)))
        
        # 偶尔有基因突变 (大变化)
        if random.random() < 0.1:
            trait = random.choice(['speed', 'caution', 'energy', 'social'])
            child_strategy[trait] = random.uniform(0, 1)
        
        # 名字变化
        if random.random() < 0.2:
            prefixes = ['Neo', 'Meta', 'Ultra', 'Crypto', 'Proto']
            name = f"{random.choice(prefixes)}{parent.name}"
        else:
            name = parent.name
        
        return Species(
            id=f"gen{self.generation}_{random.randint(1000,9999)}",
            name=name,
            strategy=child_strategy,
            fitness=parent.fitness * 0.8  # 子代适应度稍低
        )
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        alive = [s for s in self.population if s.alive]
        
        # 策略分布
        strategies = {}
        for s in alive:
            strategies[s.name] = strategies.get(s.name, 0) + 1
        
        # 平均属性
        if alive:
            avg_speed = sum(s.strategy['speed'] for s in alive) / len(alive)
            avg_caution = sum(s.strategy['caution'] for s in alive) / len(alive)
            avg_energy = sum(s.strategy['energy'] for s in alive) / len(alive)
            avg_social = sum(s.strategy['social'] for s in alive) / len(alive)
        else:
            avg_speed = avg_caution = avg_energy = avg_social = 0
        
        return {
            'generation': self.generation,
            'alive': len(alive),
            'strategies': strategies,
            'avg_speed': avg_speed,
            'avg_caution': avg_caution,
            'avg_energy': avg_energy,
            'avg_social': avg_social
        }


# ==================== 演示 ====================

def demo():
    """演示适应性进化"""
    
    print("="*70)
    print("ADAPTIVE POPULATION - Like Biology")
    print("="*70)
    
    population = AdaptivePopulation(population_size=20)
    
    # 环境变化
    environments = [
        Environment('Forest', 'speed', 0.5, 5),
        Environment('Mountain', 'caution', 0.6, 5),
        Environment('Desert', 'energy', 0.7, 5),
        Environment('Tundra', 'energy', 0.8, 5),
        Environment('Jungle', 'social', 0.5, 5),
        Environment('Chaos Realm', 'chaos', 0.9, 5),
    ]
    
    # 运行多代
    for env in environments:
        population.set_environment(env)
        
        for gen in range(5):
            # 生存挑战
            survivors = population.survive()
            
            # 繁殖
            population.reproduce(survivors)
            
            # 统计
            stats = population.get_statistics()
            
            strategy_str = ', '.join([f"{k}:{v}" for k,v in stats['strategies'].items()])
            print(f"[Gen {stats['generation']:2d}] "
                  f"Alive: {stats['alive']:2d} | "
                  f"Speed:{stats['avg_speed']:.2f} "
                  f"Caution:{stats['avg_caution']:.2f} "
                  f"Energy:{stats['avg_energy']:.2f} "
                  f"Social:{stats['avg_social']:.2f}")
    
    # 最终结果
    print("\n" + "="*70)
    print("FINAL POPULATION")
    print("="*70)
    
    stats = population.get_statistics()
    print(f"Generation: {stats['generation']}")
    print(f"Survivors: {stats['alive']}")
    print(f"\nStrategy Distribution:")
    for name, count in stats['strategies'].items():
        print(f"  {name}: {count}")
    
    print(f"\nAverage Traits:")
    print(f"  Speed: {stats['avg_speed']:.3f}")
    print(f"  Caution: {stats['avg_caution']:.3f}")
    print(f"  Energy: {stats['avg_energy']:.3f}")
    print(f"  Social: {stats['avg_social']:.3f}")


if __name__ == "__main__":
    demo()
