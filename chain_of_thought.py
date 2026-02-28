# -*- coding: utf-8 -*-
"""
Evolutionary Intelligence Swarm - Automatic Chain of Thought
自动思维链模块

核心：
1. 思维引擎推理、验证
 - 问题分解、2. 思维评估 - 深度、创造性、准确性
3. 思维遗传 - 好的思维方式传给后代
"""

import random
from typing import List, Dict, Any, Optional
from datetime import datetime


class Thought:
    """思维单元"""
    
    def __init__(self, thought_type: str, content: str):
        self.thought_type = thought_type  # question, analysis, hypothesis, reasoning, validation, conclusion
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.confidence = 0.5  # 置信度
        self.related_to = []  # 关联的思维


class ChainOfThought:
    """思维链"""
    
    def __init__(self):
        self.thoughts: List[Thought] = []
        self.current_step = 0
    
    def add(self, thought: Thought):
        """添加思维"""
        self.thoughts.append(thought)
        return self
    
    def get_chain(self) -> List[Thought]:
        """获取完整思维链"""
        return self.thoughts
    
    def get_last(self) -> Optional[Thought]:
        """获取最后思维"""
        return self.thoughts[-1] if self.thoughts else None
    
    def get_summary(self) -> str:
        """获取思维总结"""
        types = {}
        for t in self.thoughts:
            types[t.thought_type] = types.get(t.thought_type, 0) + 1
        
        return f"Steps: {len(self.thoughts)}, Types: {types}"


class ThinkingEngine:
    """思维引擎 - 核心推理能力"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
        # 思维模式
        self.thinking_modes = {
            'analytical': {
                'name': '分析思维',
                'steps': ['问题定义', '分解', '分析', '综合', '结论'],
                'weight': 0.3
            },
            'creative': {
                'name': '创造性思维',
                'steps': ['联想', '类比', '假设', '构建', '验证'],
                'weight': 0.2
            },
            'critical': {
                'name': '批判性思维',
                'steps': ['质疑', '证据', '推理', '评估', '判断'],
                'weight': 0.2
            },
            'systematic': {
                'name': '系统性思维',
                'steps': ['全局', '结构', '关系', '动态', '优化'],
                'weight': 0.15
            },
            'intuitive': {
                'name': '直觉思维',
                'steps': ['感知', '模式', '假设', '快速验证', '决策'],
                'weight': 0.15
            }
        }
    
    def think(self, problem: str, mode: str = 'analytical') -> ChainOfThought:
        """执行思维链"""
        chain = ChainOfThought()
        
        if mode not in self.thinking_modes:
            mode = 'analytical'
        
        steps = self.thinking_modes[mode]['steps']
        
        # 思维过程
        for i, step in enumerate(steps):
            thought = self._generate_thought(problem, step, i, mode)
            chain.add(thought)
        
        return chain
    
    def _generate_thought(self, problem: str, step: str, index: int, mode: str) -> Thought:
        """生成思维"""
        # 根据步骤生成内容
        templates = {
            '问题定义': f"问题是：{problem[:50]}...",
            '分解': f"将问题分解为可管理的部分",
            '分析': f"分析各个部分的特征和关系",
            '综合': f"综合各部分形成整体理解",
            '结论': f"基于分析得出结论",
            
            '联想': f"联想到相关领域：{self._random_association()}",
            '类比': f"与类似问题进行类比",
            '假设': f"提出可能的假设",
            '构建': f"构建解决方案框架",
            '验证': f"验证方案的可行性",
            
            '质疑': f"质疑现有假设的合理性",
            '证据': f"寻找支持或反驳的证据",
            '推理': f"基于证据进行逻辑推理",
            '评估': f"评估推理的有效性",
            '判断': f"做出最终判断",
            
            '全局': f"从全局视角看待问题",
            '结构': f"分析问题的结构",
            '关系': f"识别关键关系",
            '动态': f"考虑时间因素和变化",
            '优化': f"寻找最优方案",
            
            '感知': f"感知问题的关键特征",
            '模式': f"识别问题中的模式",
            '快速验证': f"快速验证核心假设",
            '决策': f"基于直觉做出决策"
        }
        
        content = templates.get(step, f"执行思维步骤: {step}")
        
        thought = Thought(step, content)
        thought.confidence = random.uniform(0.6, 0.95)
        
        return thought
    
    def _random_association(self) -> str:
        """随机联想"""
        associations = [
            "自然界中的解决方案",
            "数学中的对称性",
            "物理中的守恒定律",
            "生物中的适应机制",
            "社会中的协作模式"
        ]
        return random.choice(associations)
    
    def evolve_thinking(self, parent_thinking: Dict, mutation_rate: float = 0.3) -> Dict:
        """演化思维方式"""
        evolved = parent_thinking.copy()
        
        # 变异思维模式权重
        if random.random() < mutation_rate:
            # 调整模式权重
            for mode in evolved.get('mode_weights', {}):
                evolved['mode_weights'][mode] = max(0.05, 
                    evolved['mode_weights'][mode] + random.uniform(-0.1, 0.1))
        
        # 变异思维深度
        if random.random() < mutation_rate:
            evolved['depth'] = min(10, max(1, 
                evolved.get('depth', 5) + random.randint(-1, 1)))
        
        # 变异反思倾向
        if random.random() < mutation_rate:
            evolved['reflection'] = max(0, min(1, 
                evolved.get('reflection', 0.5) + random.uniform(-0.1, 0.1)))
        
        return evolved


class ThoughtEvaluator:
    """思维评估器"""
    
    def __init__(self):
        self.criteria = {
            'depth': {'weight': 0.25, 'name': '思维深度'},
            'logic': {'weight': 0.25, 'name': '逻辑性'},
            'creativity': {'weight': 0.2, 'name': '创造性'},
            'accuracy': {'weight': 0.2, 'name': '准确性'},
            'efficiency': {'weight': 0.1, 'name': '效率'}
        }
    
    def evaluate(self, chain: ChainOfThought) -> float:
        """评估思维链质量"""
        if not chain.thoughts:
            return 0.0
        
        scores = {}
        
        # 深度：思维步骤数
        depth_score = min(len(chain.thoughts) / 10, 1.0)
        scores['depth'] = depth_score
        
        # 逻辑性：置信度一致性
        confidences = [t.confidence for t in chain.thoughts]
        logic_score = 1.0 - (max(confidences) - min(confidences))
        scores['logic'] = logic_score
        
        # 创造性：多样性
        types = set(t.thought_type for t in chain.thoughts)
        creativity_score = min(len(types) / 5, 1.0)
        scores['creativity'] = creativity_score
        
        # 准确性：平均置信度
        accuracy_score = sum(confidences) / len(confidences)
        scores['accuracy'] = accuracy_score
        
        # 效率：步骤数/时间 (简化)
        efficiency_score = 1.0 if len(chain.thoughts) > 3 else 0.7
        scores['efficiency'] = efficiency_score
        
        # 加权总分
        total = sum(
            scores[criterion] * self.criteria[criterion]['weight']
            for criterion in self.criteria
        )
        
        return total
    
    def get_feedback(self, chain: ChainOfThought) -> List[str]:
        """获取改进建议"""
        feedback = []
        
        if len(chain.thoughts) < 5:
            feedback.append("思维深度不足，建议增加分析步骤")
        
        confidences = [t.confidence for t in chain.thoughts]
        if max(confidences) - min(confidences) > 0.3:
            feedback.append("置信度波动大，需要更一致的推理")
        
        types = set(t.thought_type for t in chain.thoughts)
        if len(types) < 3:
            feedback.append("思维模式单一，建议多元化")
        
        if not feedback:
            feedback.append("思维链质量良好")
        
        return feedback


class MetaThinker:
    """元认知 - 对思维的思考"""
    
    def __init__(self):
        self.thinking_history = []
        self.self_model = {
            'strengths': [],
            'weaknesses': [],
            'preferred_modes': [],
            'effectiveness': 0.5
        }
    
    def reflect(self, task_result: Dict, thought_chain: ChainOfThought) -> Dict:
        """反思 - 思考自己的思考"""
        # 分析结果
        success = task_result.get('success', False)
        score = task_result.get('score', 0.5)
        
        # 评估思维
        evaluator = ThoughtEvaluator()
        thought_score = evaluator.evaluate(thought_chain)
        
        # 更新自我模型
        if success and thought_score > 0.7:
            self.self_model['strengths'].append(thought_chain.get_last().thought_type)
            self.self_model['effectiveness'] = min(1.0, self.self_model['effectiveness'] + 0.05)
        elif not success or thought_score < 0.4:
            self.self_model['weaknesses'].append(thought_chain.get_last().thought_type)
            self.self_model['effectiveness'] = max(0.0, self.self_model['effectiveness'] - 0.05)
        
        # 记录
        self.thinking_history.append({
            'task': task_result.get('task', ''),
            'success': success,
            'thought_score': thought_score,
            'chain_summary': thought_chain.get_summary()
        })
        
        return {
            'reflection': f"本次思维评分: {thought_score:.2f}, 总体效能: {self.self_model['effectiveness']:.2f}",
            'strengths': self.self_model['strengths'][-3:],
            'weaknesses': self.self_model['weaknesses'][-3:],
            'suggestions': evaluator.get_feedback(thought_chain)
        }
    
    def get_preferred_mode(self) -> str:
        """获取偏好的思维模式"""
        if not self.thinking_history:
            return 'analytical'
        
        # 简单：返回历史上最成功的模式
        successful = [h for h in self.thinking_history if h['success']]
        if successful:
            return 'analytical'  # 简化处理
        return 'analytical'


# 演示
def demo():
    """演示自动思维链"""
    print("="*60)
    print("Automatic Chain of Thought Demo")
    print("="*60)
    
    # 创建思维引擎
    engine = ThinkingEngine()
    evaluator = ThoughtEvaluator()
    meta = MetaThinker()
    
    # 测试不同思维模式
    modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
    
    print("\n[1] Thinking Modes:")
    for mode in modes:
        chain = engine.think("如何优化交通流量？", mode)
        score = evaluator.evaluate(chain)
        print(f"  {mode}: {chain.get_summary()} -> Score: {score:.2f}")
    
    # 元认知反思
    print("\n[2] Meta-Cognition:")
    task_result = {'task': 'solve_traffic', 'success': True, 'score': 0.8}
    reflection = meta.reflect(task_result, chain)
    print(f"  {reflection['reflection']}")
    print(f"  Suggestions: {reflection['suggestions']}")
    
    # 思维演化
    print("\n[3] Thinking Evolution:")
    parent_thinking = {
        'mode_weights': {'analytical': 0.3, 'creative': 0.2},
        'depth': 5,
        'reflection': 0.5
    }
    evolved = engine.evolve_thinking(parent_thinking, 0.5)
    print(f"  Parent: {parent_thinking}")
    print(f"  Evolved: {evolved}")
    
    # 完整思维过程
    print("\n[4] Complete Thinking Process:")
    problem = "如何减少城市空气污染？"
    chain = engine.think(problem, 'systematic')
    
    print(f"  Problem: {problem}")
    print(f"  Chain length: {len(chain.thoughts)}")
    
    for i, thought in enumerate(chain.thoughts):
        print(f"  Step {i+1} [{thought.thought_type}]: {thought.content[:40]}... (confidence: {thought.confidence:.2f})")
    
    score = evaluator.evaluate(chain)
    print(f"\n  Total Score: {score:.2f}")
    print(f"  Feedback: {evaluator.get_feedback(chain)}")


if __name__ == "__main__":
    demo()
