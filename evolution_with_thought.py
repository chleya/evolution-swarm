# -*- coding: utf-8 -*-
"""
Evolutionary Intelligence Swarm - Complete System with Chain of Thought
演化智能群 - 完整系统(含思维链)
"""

import random
import json
from typing import List, Dict, Any, Optional


# ==================== Chain of Thought ====================

class Thought:
    def __init__(self, step: str, content: str):
        self.step = step
        self.content = content
        self.confidence = random.uniform(0.6, 0.95)


class ChainOfThought:
    def __init__(self):
        self.thoughts: List[Thought] = []
    
    def add(self, thought: Thought):
        self.thoughts.append(thought)
    
    def evaluate(self) -> float:
        if not self.thoughts:
            return 0.0
        
        # 深度
        depth = min(len(self.thoughts) / 10, 1.0)
        # 一致性
        confs = [t.confidence for t in self.thoughts]
        logic = 1.0 - (max(confs) - min(confs))
        # 多样性
        diversity = min(len(set(t.step for t in self.thoughts)) / 5, 1.0)
        # 置信度
        accuracy = sum(confs) / len(confs)
        
        return depth * 0.25 + logic * 0.25 + diversity * 0.2 + accuracy * 0.3


# ==================== Thinking Engine ====================

class ThinkingEngine:
    """思维引擎"""
    
    MODES = {
        'analytical': ['问题定义', '分解', '分析', '综合', '结论'],
        'creative': ['联想', '类比', '假设', '构建', '验证'],
        'critical': ['质疑', '证据', '推理', '评估', '判断'],
        'systematic': ['全局', '结构', '关系', '动态', '优化'],
        'intuitive': ['感知', '模式', '假设', '快速验证', '决策']
    }
    
    def think(self, problem: str, mode: str = 'analytical') -> ChainOfThought:
        """执行思维"""
        chain = ChainOfThought()
        steps = self.MODES.get(mode, self.MODES['analytical'])
        
        for step in steps:
            thought = Thought(step, f"[{step}] {problem[:30]}...")
            chain.add(thought)
        
        return chain
    
    def evolve(self, thinking: Dict, rate: float = 0.3) -> Dict:
        """演化思维方式"""
        evolved = thinking.copy()
        
        if random.random() < rate:
            evolved['depth'] = min(10, max(1, evolved.get('depth', 5) + random.randint(-1, 1)))
        
        if random.random() < rate:
            evolved['preferred_mode'] = random.choice(list(self.MODES.keys()))
        
        return evolved


# ==================== Gene Operator ====================

class GeneOperator:
    def __init__(self):
        self.roles = ['explorer', 'builder', 'analyzer', 'negotiator']
        self.tools = ['browser', 'bash', 'read', 'write', 'edit']
        self.thinking_modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
    
    def mutate(self, variant: Dict, rate: float = 0.3) -> Dict:
        mutated = variant.copy()
        mutated['variant_id'] = f"variant_{random.randint(10000,99999)}"
        mutated['generation'] = variant.get('generation', 0) + 1
        
        # 基因变异
        if random.random() < rate:
            mutated['genome']['cognitive']['role'] = random.choice(self.roles)
        
        if random.random() < rate:
            mutated['genome']['thinking']['mode'] = random.choice(self.thinking_modes)
        
        if random.random() < rate:
            mutated['genome']['thinking']['depth'] = min(10, max(1, 
                mutated['genome']['thinking'].get('depth', 5) + random.randint(-1, 1)))
        
        # 重置表现型
        mutated['phenotype'] = {
            'fitness': 0.0,
            'thought_score': 0.0,
            'tasks': 0,
            'alive': True
        }
        
        return mutated
    
    def crossover(self, p1: Dict, p2: Dict) -> Dict:
        child = {
            'variant_id': f"variant_{random.randint(10000,99999)}",
            'generation': max(p1.get('generation', 0), p2.get('generation', 0)) + 1,
            'genome': {},
            'phenotype': {'fitness': 0.0, 'thought_score': 0.0, 'tasks': 0, 'alive': True}
        }
        
        # 均匀交叉
        for key in p1['genome']:
            child['genome'][key] = p1['genome'][key] if random.random() < 0.5 else p2['genome'].get(key, {})
        
        return child


# ==================== Fitness Evaluator ====================

class FitnessEvaluator:
    def __init__(self):
        self.weights = {
            'task': 0.4,
            'thinking': 0.4,
            'efficiency': 0.2
        }
    
    def calculate(self, variant: Dict, metrics: Dict) -> float:
        # 任务得分
        tasks = metrics.get('tasks', 0)
        errors = metrics.get('errors', 0)
        task_score = max(0, min(1, tasks / 10 - errors * 0.1))
        
        # 思维得分
        thought_score = metrics.get('thought_score', 0.5)
        
        # 效率
        resources = metrics.get('resources', 100)
        efficiency = tasks / max(resources, 1)
        
        total = (
            task_score * self.weights['task'] +
            thought_score * self.weights['thinking'] +
            efficiency * self.weights['efficiency']
        )
        
        return max(0, min(1, total))


# ==================== Evolution Scheduler ====================

class EvolutionScheduler:
    def __init__(self, config: Dict):
        self.config = config
        self.gene_op = GeneOperator()
        self.fitness_eval = FitnessEvaluator()
        self.thinking = ThinkingEngine()
        self.population: List[Dict] = []
        self.generation = 0
    
    def init(self, seeds: List[str]):
        for i, seed in enumerate(seeds):
            variant = {
                'variant_id': f"seed_{i}",
                'generation': 0,
                'genome': {
                    'cognitive': {
                        'role': random.choice(['explorer', 'builder', 'analyzer']),
                        'prompt': seed,
                        'tools': random.sample(['browser', 'read', 'write'], 2)
                    },
                    'thinking': {
                        'mode': random.choice(['analytical', 'creative', 'systematic']),
                        'depth': random.randint(3, 7),
                        'reflection': random.uniform(0.3, 0.7)
                    },
                    'social': {
                        'style': random.choice(['direct', 'collaborative']),
                        'cooperation': random.uniform(0.4, 0.8)
                    }
                },
                'phenotype': {
                    'fitness': 0.0,
                    'thought_score': 0.0,
                    'tasks': 0,
                    'alive': True
                }
            }
            self.population.append(variant)
        
        # 填充
        while len(self.population) < self.config['population_size']:
            p = random.choice(self.population)
            self.population.append(self.gene_op.mutate(p, 1.0))
        
        print(f"[Init] Population: {len(self.population)}")
    
    def evolve(self):
        self.generation += 1
        print(f"\n=== Generation {self.generation} ===")
        
        # 选择
        sorted_pop = sorted(self.population, key=lambda x: x['phenotype']['fitness'], reverse=True)
        elite = sorted_pop[:max(2, len(sorted_pop) // 5)]
        
        # 生成新一代
        new_pop = list(elite)
        
        while len(new_pop) < self.config['population_size']:
            if random.random() < self.config['crossover_rate']:
                p1, p2 = random.sample(elite, 2)
                child = self.gene_op.crossover(p1, p2)
            else:
                parent = random.choice(elite)
                child = self.gene_op.mutate(parent, self.config['mutation_rate'])
            new_pop.append(child)
        
        self.population = new_pop
        
        # 统计
        fitness = [v['phenotype']['fitness'] for v in self.population]
        thought = [v['phenotype']['thought_score'] for v in self.population]
        
        print(f"Avg Fitness: {sum(fitness)/len(fitness):.3f}")
        print(f"Avg Thought: {sum(thought)/len(thought):.3f}")
        print(f"Best: {max(fitness):.3f}")
    
    def update(self, variant_id: str, metrics: Dict):
        for v in self.population:
            if v['variant_id'] == variant_id:
                v['phenotype']['fitness'] = self.fitness_eval.calculate(v, metrics)
                v['phenotype']['thought_score'] = metrics.get('thought_score', 0.5)
                v['phenotype']['tasks'] = metrics.get('tasks', 0)
                break
    
    def think(self, variant_id: str, problem: str) -> ChainOfThought:
        for v in self.population:
            if v['variant_id'] == variant_id:
                mode = v['genome']['thinking']['mode']
                return self.thinking.think(problem, mode)
        return self.thinking.think(problem, 'analytical')
    
    def get_best(self) -> Optional[Dict]:
        if not self.population:
            return None
        return max(self.population, key=lambda x: x['phenotype']['fitness'])


# ==================== Demo ====================

def demo():
    print("="*60)
    print("Evolutionary Swarm with Chain of Thought")
    print("="*60)
    
    # 配置
    config = {
        'population_size': 10,
        'mutation_rate': 0.3,
        'crossover_rate': 0.5
    }
    
    # 初始化
    seeds = [
        "你是一个探索者，发现新知识",
        "你是一个分析者，深挖问题",
        "你是一个构建者，创造方案"
    ]
    
    scheduler = EvolutionScheduler(config)
    scheduler.init(seeds)
    
    # 演化几代
    for gen in range(5):
        # 模拟每个变体的任务
        for variant in scheduler.population:
            # 思维
            chain = scheduler.think(variant['variant_id'], "如何优化这个系统？")
            thought_score = chain.evaluate()
            
            # 任务指标
            metrics = {
                'tasks': random.randint(1, 10),
                'errors': random.randint(0, 3),
                'resources': random.randint(50, 200),
                'thought_score': thought_score
            }
            
            scheduler.update(variant['variant_id'], metrics)
        
        scheduler.evolve()
    
    # 结果
    print("\n" + "="*60)
    print("Final Result")
    print("="*60)
    
    best = scheduler.get_best()
    if best:
        print(f"Best Variant: {best['variant_id']}")
        print(f"  Generation: {best['generation']}")
        print(f"  Role: {best['genome']['cognitive']['role']}")
        print(f"  Thinking Mode: {best['genome']['thinking']['mode']}")
        print(f"  Thinking Depth: {best['genome']['thinking']['depth']}")
        print(f"  Fitness: {best['phenotype']['fitness']:.3f}")
        print(f"  Thought Score: {best['phenotype']['thought_score']:.3f}")
        
        # 展示思维
        print(f"\nThinking Process:")
        chain = scheduler.think(best['variant_id'], "如何解决交通拥堵？")
        for i, t in enumerate(chain.thoughts):
            print(f"  {i+1}. [{t.step}] confidence: {t.confidence:.2f}")
        print(f"  Total Score: {chain.evaluate():.3f}")


if __name__ == "__main__":
    demo()
