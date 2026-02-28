# -*- coding: utf-8 -*-
"""
Evolutionary Swarm - Deep Thinking System
深度思维系统 - 真实问题解决
"""

import random
import math
from typing import List, Dict, Any, Optional
from datetime import datetime


class Problem:
    """问题库"""
    
    PROBLEMS = [
        {
            'id': 'math_1',
            'type': 'math',
            'question': '求解: 2x + 5 = 15',
            'answer': 'x = 5',
            'difficulty': 1
        },
        {
            'id': 'math_2', 
            'type': 'math',
            'question': '求解: x^2 - 4 = 0',
            'answer': 'x = 2 或 x = -2',
            'difficulty': 2
        },
        {
            'id': 'logic_1',
            'type': 'logic',
            'question': '如果所有A是B, 所有B是C, 那么所有A是C吗?',
            'answer': '是的, 这是传递性',
            'difficulty': 2
        },
        {
            'id': 'puzzle_1',
            'type': 'puzzle',
            'question': '有100个球, 其中1个比其他的重, 用天平最少称几次?',
            'answer': '5次 (log3 100 ≈ 5)',
            'difficulty': 3
        },
        {
            'id': 'algorithm_1',
            'type': 'algorithm',
            'question': '如何快速查找排序数组中的元素?',
            'answer': '二分查找 O(log n)',
            'difficulty': 3
        }
    ]
    
    @classmethod
    def get_random(cls, difficulty=None):
        problems = cls.PROBLEMS
        if difficulty:
            problems = [p for p in problems if p['difficulty'] <= difficulty]
        return random.choice(problems)


class DeepThinker:
    """深度思考者"""
    
    def __init__(self, variant_id: str, genome: Dict):
        self.variant_id = variant_id
        self.genome = genome
        self.thinking_history = []
        self.successes = 0
        self.failures = 0
    
    def solve(self, problem: Problem) -> Dict:
        """解决问题 - 展示思维链"""
        
        mode = self.genome['thinking']['mode']
        depth = self.genome['thinking']['depth']
        
        # 思维链记录
        thought_chain = []
        
        # 根据模式生成不同思维过程
        if mode == 'analytical':
            thought_chain = self._analytical_solve(problem, depth)
        elif mode == 'creative':
            thought_chain = self._creative_solve(problem, depth)
        elif mode == 'critical':
            thought_chain = self._critical_solve(problem, depth)
        elif mode == 'systematic':
            thought_chain = self._systematic_solve(problem, depth)
        elif mode == 'intuitive':
            thought_chain = self._intuitive_solve(problem, depth)
        
        # 评估思维质量
        thought_quality = self._evaluate_thinking(thought_chain, problem)
        
        # 判断答案 - 加入随机性
        correct = self._check_answer(problem, thought_quality)
        
        # 记录
        self.thinking_history.append({
            'problem': problem['id'],
            'mode': mode,
            'depth': depth,
            'thought_chain': thought_chain,
            'quality': thought_quality,
            'correct': correct,
            'timestamp': datetime.now().isoformat()
        })
        
        if correct:
            self.successes += 1
        else:
            self.failures += 1
        
        return {
            'variant_id': self.variant_id,
            'problem': problem['question'],
            'thinking': thought_chain,
            'quality': thought_quality,
            'correct': correct,
            'mode': mode
        }
    
    def _analytical_solve(self, problem: Dict, depth: int) -> List[Dict]:
        """分析思维"""
        thoughts = []
        
        thoughts.append({
            'step': '理解问题',
            'content': f"问题是: {problem['question']}",
            'confidence': 0.9
        })
        
        thoughts.append({
            'step': '分解问题',
            'content': '将问题分解为已知和未知部分',
            'confidence': 0.85
        })
        
        # 深度决定步骤数
        if depth >= 3:
            thoughts.append({
                'step': '识别模式',
                'content': '识别问题类型: ' + problem['type'],
                'confidence': 0.8
            })
        
        if depth >= 5:
            thoughts.append({
                'step': '建立模型',
                'content': '建立数学/逻辑模型',
                'confidence': 0.75
            })
        
        thoughts.append({
            'step': '求解',
            'content': f"得出答案: {problem['answer']}",
            'confidence': 0.7
        })
        
        return thoughts
    
    def _creative_solve(self, problem: Dict, depth: int) -> List[Dict]:
        """创造性思维"""
        thoughts = []
        
        thoughts.append({
            'step': '联想',
            'content': f"联想到类似问题: {problem['type']}",
            'confidence': 0.8
        })
        
        thoughts.append({
            'step': '类比',
            'content': '尝试用不同方法解决',
            'confidence': 0.75
        })
        
        thoughts.append({
            'step': '假设',
            'content': '提出多种可能的解法',
            'confidence': 0.7
        })
        
        if depth >= 5:
            thoughts.append({
                'step': '创新',
                'content': '尝试非常规方法',
                'confidence': 0.65
            })
        
        thoughts.append({
            'step': '验证',
            'content': f"验证答案: {problem['answer']}",
            'confidence': 0.8
        })
        
        return thoughts
    
    def _critical_solve(self, problem: Dict, depth: int) -> List[Dict]:
        """批判性思维"""
        thoughts = []
        
        thoughts.append({
            'step': '质疑',
            'content': '这个问题的前提是什么?',
            'confidence': 0.85
        })
        
        thoughts.append({
            'step': '分析假设',
            'content': '验证假设的合理性',
            'confidence': 0.8
        })
        
        thoughts.append({
            'step': '逻辑检查',
            'content': '检查推理过程',
            'confidence': 0.9
        })
        
        thoughts.append({
            'step': '评估',
            'content': '评估解法的有效性',
            'confidence': 0.85
        })
        
        thoughts.append({
            'step': '判断',
            'content': f"最终答案: {problem['answer']}",
            'confidence': 0.75
        })
        
        return thoughts
    
    def _systematic_solve(self, problem: Dict, depth: int) -> List[Dict]:
        """系统性思维"""
        thoughts = []
        
        thoughts.append({
            'step': '全局',
            'content': '从整体把握问题结构',
            'confidence': 0.9
        })
        
        thoughts.append({
            'step': '结构',
            'content': '分析问题的组成部分',
            'confidence': 0.85
        })
        
        thoughts.append({
            'step': '关系',
            'content': '理解各部分之间的关系',
            'confidence': 0.8
        })
        
        thoughts.append({
            'step': '动态',
            'content': '考虑时间和变化因素',
            'confidence': 0.75
        })
        
        thoughts.append({
            'step': '优化',
            'content': f"找到最优解: {problem['answer']}",
            'confidence': 0.7
        })
        
        return thoughts
    
    def _intuitive_solve(self, problem: Dict, depth: int) -> List[Dict]:
        """直觉思维"""
        thoughts = []
        
        thoughts.append({
            'step': '感知',
            'content': '快速感知问题关键',
            'confidence': 0.7
        })
        
        thoughts.append({
            'step': '模式识别',
            'content': '识别问题中的模式',
            'confidence': 0.75
        })
        
        thoughts.append({
            'step': '直觉判断',
            'content': '凭直觉给出答案',
            'confidence': 0.6
        })
        
        thoughts.append({
            'step': '快速验证',
            'content': '快速验证答案合理性',
            'confidence': 0.8
        })
        
        thoughts.append({
            'step': '决策',
            'content': f"确定: {problem['answer']}",
            'confidence': 0.7
        })
        
        return thoughts
    
    def _evaluate_thinking(self, thoughts: List[Dict], problem: Dict) -> float:
        """评估思维质量"""
        if not thoughts:
            return 0.0
        
        # 深度得分
        depth_score = min(len(thoughts) / 10, 1.0)
        
        # 置信度一致性
        confs = [t['confidence'] for t in thoughts]
        consistency = 1.0 - (max(confs) - min(confs))
        
        # 步骤合理性
        completeness = len(thoughts) / 5  # 期望5步
        
        return depth_score * 0.3 + consistency * 0.3 + completeness * 0.4
    
    def _check_answer(self, problem: Problem, thought_quality: float) -> bool:
        """检查答案 - 真实难度模拟"""
        difficulty = problem['difficulty']
        
        # 基准难度: 简单=30%, 中等=20%, 难=10%
        base_rates = {1: 0.70, 2: 0.50, 3: 0.30}
        base = base_rates.get(difficulty, 0.3)
        
        # 思维模式加成
        mode = self.genome['thinking']['mode']
        if mode == 'critical' and difficulty <= 2:
            base += 0.25  # 批判性思维对简单/中等问题很有效
        elif mode == 'analytical':
            base += 0.20
        elif mode == 'systematic':
            base += 0.15
        elif mode == 'intuitive':
            base -= 0.10  # 直觉对难题更差
        
        # 深度加成
        depth = self.genome['thinking']['depth']
        if depth >= 5:
            base += 0.10
        elif depth < 3:
            base -= 0.10
        
        # 思维质量影响
        base += thought_quality * 0.15
        
        # 限制范围
        rate = max(0.05, min(0.95, base))
        
        return random.random() < rate
    
    def get_stats(self) -> Dict:
        total = self.successes + self.failures
        return {
            'variant_id': self.variant_id,
            'successes': self.successes,
            'failures': self.failures,
            'success_rate': self.successes / max(total, 1),
            'mode': self.genome['thinking']['mode'],
            'depth': self.genome['thinking']['depth']
        }


class EvolutionWithProblems:
    """演化系统 - 真实问题解决"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.population: List[DeepThinker] = []
        self.generation = 0
        self.history = []
    
    def init_population(self):
        """初始化种群"""
        modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
        
        for i in range(self.config['population_size']):
            genome = {
                'thinking': {
                    'mode': random.choice(modes),
                    'depth': random.randint(3, 8),
                    'reflection': random.uniform(0.3, 0.7)
                },
                'cognitive': {
                    'role': random.choice(['explorer', 'builder', 'analyzer'])
                }
            }
            
            variant_id = f"gen{self.generation}_variant_{i}"
            thinker = DeepThinker(variant_id, genome)
            self.population.append(thinker)
        
        print(f"[Init] Created {len(self.population)} thinkers")
    
    def solve_problems(self, num_problems: int = 3):
        """让所有思考者解决问题"""
        results = []
        
        for thinker in self.population:
            for _ in range(num_problems):
                problem = Problem.get_random()
                result = thinker.solve(problem)
                results.append(result)
        
        return results
    
    def evolve(self):
        """演化一代"""
        self.generation += 1
        
        # 评估适应度
        scored = []
        for thinker in self.population:
            stats = thinker.get_stats()
            score = stats['success_rate'] * 0.6 + stats.get('quality', 0.5) * 0.4
            scored.append((thinker, score))
        
        # 选择精英
        scored.sort(key=lambda x: x[1], reverse=True)
        elite = [s[0] for s in scored[:max(2, len(scored) // 5)]]
        
        # 生成新一代
        new_population = []
        
        # 保留精英
        new_population.extend(elite)
        
        # 变异/交叉
        while len(new_population) < self.config['population_size']:
            parent = random.choice(elite)
            
            # 变异
            child_genome = {
                'thinking': {
                    'mode': parent.genome['thinking']['mode'],
                    'depth': parent.genome['thinking']['depth'],
                    'reflection': parent.genome['thinking']['reflection']
                },
                'cognitive': parent.genome['cognitive'].copy()
            }
            
            # 变异思维
            if random.random() < self.config['mutation_rate']:
                child_genome['thinking']['mode'] = random.choice(
                    ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
                )
            
            if random.random() < self.config['mutation_rate']:
                child_genome['thinking']['depth'] = min(10, max(1,
                    child_genome['thinking']['depth'] + random.randint(-1, 1)))
            
            child_id = f"gen{self.generation}_variant_{len(new_population)}"
            child = DeepThinker(child_id, child_genome)
            new_population.append(child)
        
        self.population = new_population
        
        # 统计
        total_success = sum(t.successes for t in self.population)
        total_trials = sum(t.successes + t.failures for t in self.population)
        avg_rate = total_success / max(total_trials, 1)
        
        best = max(scored, key=lambda x: x[1])
        
        print(f"[Gen {self.generation}] Success Rate: {avg_rate:.2%}, Best Mode: {best[0].genome['thinking']['mode']}")
        
        self.history.append({
            'generation': self.generation,
            'success_rate': avg_rate,
            'best_mode': best[0].genome['thinking']['mode'],
            'best_depth': best[0].genome['thinking']['depth']
        })


def demo():
    print("="*60)
    print("Deep Thinking Problem Solving Demo")
    print("="*60)
    
    config = {
        'population_size': 10,
        'mutation_rate': 0.4
    }
    
    system = EvolutionWithProblems(config)
    system.init_population()
    
    # 演化多代
    for gen in range(8):
        # 解决问题
        results = system.solve_problems(3)
        
        # 演化
        system.evolve()
    
    # 最终展示
    print("\n" + "="*60)
    print("Final Results")
    print("="*60)
    
    # 最佳思考者
    best = max(system.population, key=lambda t: t.successes)
    stats = best.get_stats()
    
    print(f"\nBest Thinker: {stats['variant_id']}")
    print(f"  Mode: {stats['mode']}")
    print(f"  Depth: {stats['depth']}")
    print(f"  Success Rate: {stats['success_rate']:.1%}")
    print(f"  ({stats['successes']}/{stats['successes']+stats['failures']})")
    
    # 展示最佳思考者的思维
    print(f"\nThinking Process:")
    if best.thinking_history:
        thought = best.thinking_history[-1]
        if 'thinking' in thought:
            for t in thought['thinking']:
                print(f"  [{t['step']}] {t['content'][:50]}... (conf: {t['confidence']:.2f})")
        else:
            print(f"  (thinking data unavailable)")
    
    # 演化趋势
    print(f"\nEvolution Trend:")
    for h in system.history:
        print(f"  Gen {h['generation']}: {h['success_rate']:.1%} (best: {h['best_mode']}, depth={h['best_depth']})")


if __name__ == "__main__":
    demo()
