# -*- coding: utf-8 -*-
"""
Evolutionary Intelligence Swarm - MVP
演化智能群 - 最小可行产品

核心功能：
1. 智能体变体管理
2. 基因变异/重组
3. 适应度评估
4. 演化调度
"""

import random
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class GeneOperator:
    """基因操作器 - 变异和重组"""
    
    def __init__(self):
        self.roles = ['explorer', 'builder', 'analyzer', 'negotiator']
        self.tools = ['browser', 'bash', 'read', 'write', 'edit']
        self.styles = ['direct', 'diplomatic', 'assertive', 'collaborative']
    
    def mutate(self, variant: Dict, mutation_rate: float = 0.3) -> Dict:
        """变异 - 随机改变基因"""
        mutated = variant.copy()
        mutated['variant_id'] = f"variant_{int(time.time())}_{random.randint(1000,9999)}"
        mutated['generation'] = variant.get('generation', 0) + 1
        mutated['parent_ids'] = [variant['variant_id']]
        mutated['created_at'] = datetime.now().isoformat()
        
        # 重置表现型
        mutated['phenotype'] = {
            'fitness': 0.0,
            'tasks_completed': 0,
            'resources_used': 0,
            'alive': True
        }
        
        # 变异认知基因
        if random.random() < mutation_rate:
            mutated['genome']['cognitive']['role'] = random.choice(self.roles)
        
        if random.random() < mutation_rate:
            mutated['genome']['cognitive']['tools'] = random.sample(
                self.tools, random.randint(1, 3)
            )
        
        # 变异社交基因
        if random.random() < mutation_rate:
            mutated['genome']['social']['style'] = random.choice(self.styles)
        
        if random.random() < mutation_rate:
            mutated['genome']['social']['cooperation'] = random.uniform(0.3, 0.9)
        
        # 变异适应基因
        if random.random() < mutation_rate:
            mutated['genome']['adaptive']['learning_rate'] = random.uniform(0.01, 0.2)
        
        if random.random() < mutation_rate:
            mutated['genome']['adaptive']['explore_ratio'] = random.uniform(0.3, 0.8)
        
        return mutated
    
    def crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """重组 - 合并两个亲本的基因"""
        child = {
            'variant_id': f"variant_{int(time.time())}_{random.randint(1000,9999)}",
            'generation': max(parent1.get('generation', 0), parent2.get('generation', 0)) + 1,
            'parent_ids': [parent1['variant_id'], parent2['variant_id']],
            'created_at': datetime.now().isoformat(),
            'genome': {
                'cognitive': {},
                'social': {},
                'adaptive': {}
            },
            'phenotype': {
                'fitness': 0.0,
                'tasks_completed': 0,
                'resources_used': 0,
                'alive': True
            }
        }
        
        # 均匀交叉
        for key in child['genome']['cognitive']:
            child['genome']['cognitive'][key] = (
                parent1['genome']['cognitive'].get(key) 
                if random.random() < 0.5 
                else parent2['genome']['cognitive'].get(key)
            )
        
        for key in child['genome']['social']:
            child['genome']['social'][key] = (
                parent1['genome']['social'].get(key)
                if random.random() < 0.5
                else parent2['genome']['social'].get(key)
            )
        
        for key in child['genome']['adaptive']:
            child['genome']['adaptive'][key] = (
                parent1['genome']['adaptive'].get(key)
                if random.random() < 0.5
                else parent2['genome']['adaptive'].get(key)
            )
        
        return child


class FitnessEvaluator:
    """适应度评估器"""
    
    def __init__(self):
        self.weights = {
            'task_success': 0.5,
            'efficiency': 0.3,
            'stability': 0.2
        }
    
    def calculate(self, variant: Dict, metrics: Dict) -> float:
        """计算适应度"""
        # 任务成功率
        tasks = metrics.get('tasks_completed', 0)
        errors = metrics.get('errors', 0)
        task_score = min(tasks / 10, 1.0) if tasks > 0 else 0
        task_score -= (errors / max(tasks, 1)) * 0.3
        
        # 效率
        resources = metrics.get('resources_used', 1)
        efficiency = tasks / max(resources, 1)
        efficiency_score = min(efficiency / 10, 1.0)
        
        # 稳定性
        stability_score = 1.0 if errors == 0 else max(0, 1 - errors / 5)
        
        # 加权求和
        fitness = (
            task_score * self.weights['task_success'] +
            efficiency_score * self.weights['efficiency'] +
            stability_score * self.weights['stability']
        )
        
        return max(0, min(1, fitness))


class EvolutionScheduler:
    """演化调度器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.gene_operator = GeneOperator()
        self.fitness_evaluator = FitnessEvaluator()
        self.population: List[Dict] = []
        self.generation = 0
        self.history = []
    
    def initialize_population(self, seed_prompts: List[str]):
        """初始化种群"""
        print(f"[Scheduler] 初始化种群，大小: {self.config['population_size']}")
        
        # 从种子生成初始种群
        for i, prompt in enumerate(seed_prompts):
            variant = {
                'variant_id': f"seed_{i}_{int(time.time())}",
                'generation': 0,
                'parent_ids': [],
                'created_at': datetime.now().isoformat(),
                'genome': {
                    'cognitive': {
                        'role': random.choice(['explorer', 'builder', 'analyzer']),
                        'prompt': prompt,
                        'tools': random.sample(['browser', 'bash', 'read', 'write'], 2)
                    },
                    'social': {
                        'style': random.choice(['direct', 'diplomatic', 'collaborative']),
                        'cooperation': random.uniform(0.4, 0.8)
                    },
                    'adaptive': {
                        'learning_rate': random.uniform(0.05, 0.15),
                        'explore_ratio': random.uniform(0.4, 0.7)
                    }
                },
                'phenotype': {
                    'fitness': 0.0,
                    'tasks_completed': 0,
                    'resources_used': 0,
                    'alive': True
                }
            }
            self.population.append(variant)
        
        # 变异填充到目标大小
        while len(self.population) < self.config['population_size']:
            parent = random.choice(self.population)
            mutated = self.gene_operator.mutate(parent, self.config['mutation_rate'])
            self.population.append(mutated)
        
        print(f"[Scheduler] 种群初始化完成: {len(self.population)} 个变体")
    
    def select(self) -> List[Dict]:
        """选择 - 精英保留 + 锦标赛"""
        # 精英保留
        sorted_pop = sorted(self.population, key=lambda x: x['phenotype']['fitness'], reverse=True)
        elite_count = int(len(self.population) * self.config['elite_ratio'])
        selected = sorted_pop[:elite_count]
        
        # 锦标赛选择填充
        while len(selected) < len(self.population):
            tournament = random.sample(self.population, 3)
            winner = max(tournament, key=lambda x: x['phenotype']['fitness'])
            selected.append(winner)
        
        return selected
    
    def evolve(self):
        """演化一代"""
        self.generation += 1
        print(f"\n[Scheduler] === 第 {self.generation} 代 ===")
        
        # 选择
        selected = self.select()
        
        # 生成新一代
        new_population = []
        
        # 保留精英
        elite_count = int(len(self.population) * self.config['elite_ratio'])
        new_population.extend(selected[:elite_count])
        
        # 变异和重组
        while len(new_population) < self.config['population_size']:
            if random.random() < self.config['crossover_rate']:
                # 交叉
                p1, p2 = random.sample(selected, 2)
                child = self.gene_operator.crossover(p1, p2)
            else:
                # 变异
                parent = random.choice(selected)
                child = self.gene_operator.mutate(parent, self.config['mutation_rate'])
            
            new_population.append(child)
        
        self.population = new_population
        
        # 记录历史
        avg_fitness = sum(v['phenotype']['fitness'] for v in self.population) / len(self.population)
        best_fitness = max(v['phenotype']['fitness'] for v in self.population)
        
        self.history.append({
            'generation': self.generation,
            'avg_fitness': avg_fitness,
            'best_fitness': best_fitness,
            'population_size': len(self.population)
        })
        
        print(f"[Scheduler] 平均适应度: {avg_fitness:.3f}, 最佳: {best_fitness:.3f}")
        
        return self.population
    
    def update_fitness(self, variant_id: str, metrics: Dict):
        """更新个体适应度"""
        for variant in self.population:
            if variant['variant_id'] == variant_id:
                fitness = self.fitness_evaluator.calculate(variant, metrics)
                variant['phenotype']['fitness'] = fitness
                variant['phenotype']['tasks_completed'] = metrics.get('tasks_completed', 0)
                variant['phenotype']['resources_used'] = metrics.get('resources_used', 1)
                break
    
    def get_best_variant(self) -> Optional[Dict]:
        """获取最佳变体"""
        if not self.population:
            return None
        return max(self.population, key=lambda x: x['phenotype']['fitness'])
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.population:
            return {}
        
        fitness_values = [v['phenotype']['fitness'] for v in self.population]
        
        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'avg_fitness': sum(fitness_values) / len(fitness_values),
            'best_fitness': max(fitness_values),
            'worst_fitness': min(fitness_values)
        }


# 演示
def demo():
    """演示演化过程"""
    print("="*60)
    print("Evolutionary Intelligence Swarm - Demo")
    print("="*60)
    
    # 配置
    config = {
        'population_size': 10,
        'elite_ratio': 0.2,
        'mutation_rate': 0.3,
        'crossover_rate': 0.5
    }
    
    # 种子Prompt
    seed_prompts = [
        "你是一个勇敢的探索者，发现新事物",
        "你是一个严谨的分析者，检查细节",
        "你是一个创造者，构建新方案"
    ]
    
    # 创建调度器
    scheduler = EvolutionScheduler(config)
    scheduler.initialize_population(seed_prompts)
    
    # 模拟演化
    for gen in range(5):
        # 模拟每个变体的表现
        for variant in scheduler.population:
            # 随机生成指标
            metrics = {
                'tasks_completed': random.randint(0, 10),
                'errors': random.randint(0, 3),
                'resources_used': random.randint(50, 200)
            }
            scheduler.update_fitness(variant['variant_id'], metrics)
        
        # 演化一代
        scheduler.evolve()
    
    # 最终结果
    print("\n" + "="*60)
    print("最终结果")
    print("="*60)
    
    stats = scheduler.get_stats()
    print(f"代数: {stats['generation']}")
    print(f"种群大小: {stats['population_size']}")
    print(f"平均适应度: {stats['avg_fitness']:.3f}")
    print(f"最佳适应度: {stats['best_fitness']:.3f}")
    
    best = scheduler.get_best_variant()
    print(f"\nBest Variant:")
    print(f"  ID: {best['variant_id']}")
    print(f"  Generation: {best['generation']}")
    print(f"  Fitness: {best['phenotype']['fitness']:.3f}")


if __name__ == "__main__":
    demo()
