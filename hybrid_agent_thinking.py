# -*- coding: utf-8 -*-
"""
Hybrid Thinking + OpenClaw Agent - 任务驱动 + 自主思维 + 真实Agent
"""

import random
import time
from datetime import datetime
from typing import List, Dict


class ThoughtNode:
    def __init__(self, content: str, type: str):
        self.content = content
        self.type = type
        self.children: List['ThoughtNode'] = []
        self.timestamp = datetime.now().isoformat()


class Task:
    def __init__(self, id: str, name: str, prompt: str, priority: int = 5):
        self.id = id
        self.name = name
        self.prompt = prompt
        self.priority = priority
        self.status = "pending"
        self.result = None
        self.thought_chain = []


class HybridAgentThinker:
    """混合思维Agent - 接入真实OpenClaw"""
    
    def __init__(self, name: str = "Thinker"):
        self.name = name
        self.task_queue: List[Task] = []
        self.mode = "idle"
        self.cycles = 0
        self.self_modes = ['analyze', 'question', 'hypothesize', 'connect', 'reflect']
        
        # 思维模式配置
        self.thinking_configs = {
            'analytical': {
                'role': '分析者',
                'system': '你是一个严谨的分析者，擅长分解问题、逻辑推理。'
            },
            'creative': {
                'role': '创造者',
                'system': '你是一个富有创造力的思考者，擅长联想、假设、创新。'
            },
            'critical': {
                'role': '批判者',
                'system': '你是一个批判性思考者，擅长质疑、分析漏洞、验证假设。'
            },
            'systematic': {
                'role': '系统思考者',
                'system': '你是一个系统性思考者，擅长全局视角、关系分析、动态思维。'
            },
            'intuitive': {
                'role': '直觉思考者',
                'system': '你是一个直觉敏锐的思考者，擅长快速模式识别和直觉判断。'
            }
        }
    
    def run_forever(self, max_cycles: int = 10):
        print(f"\n{'='*60}")
        print(f"{self.name} 启动 - 任务驱动 + 自主思维 + Agent执行")
        print(f"{'='*60}\n")
        
        while self.cycles < max_cycles:
            self.cycles += 1
            
            if self.task_queue:
                task = self.get_next_task()
                self.execute_task_with_agent(task)
            else:
                self.autonomous_think()
            
            time.sleep(0.3)
        
        print(f"\n停止，共 {self.cycles} 轮")
    
    def get_next_task(self) -> Task:
        self.task_queue.sort(key=lambda t: -t.priority)
        task = self.task_queue.pop(0)
        task.status = "running"
        return task
    
    def add_task(self, task: Task):
        self.task_queue.append(task)
        print(f"\n[TASK] {task.name} (priority: {task.priority})")
    
    def execute_task_with_agent(self, task: Task):
        """用Agent执行任务 - 展示思维链"""
        self.mode = "tasking"
        
        print(f"\n{'-'*40}")
        print(f"[EXEC] {task.name}")
        print(f"{'-'*40}")
        
        # 1. 选择思维模式
        thinking_mode = random.choice(list(self.thinking_configs.keys()))
        config = self.thinking_configs[thinking_mode]
        
        print(f"  -> 选择思维模式: {config['role']}")
        
        # 2. 展示任务理解思维
        task.thought_chain = []
        
        thought1 = ThoughtNode(f"理解任务: {task.name}", "understand")
        task.thought_chain.append(thought1)
        print(f"  -> 理解任务...")
        
        # 3. 思维展开
        current = thought1
        for i, mode_name in enumerate(['question', 'analyze', 'hypothesize', 'connect']):
            child = self._create_thought_node(mode_name, f"步骤{i+1}")
            current.children.append(child)
            task.thought_chain.append(child)
            current = child
            
            mode_label = {
                'question': '提问',
                'analyze': '分析', 
                'hypothesize': '假设',
                'connect': '联想'
            }.get(mode_name, mode_name)
            
            print(f"  -> {mode_label}...")
        
        # 4. 调用Agent (模拟)
        print(f"  -> 调用Agent: {config['role']}")
        
        # 生成Agent提示词
        agent_prompt = f"""{config['system']}

任务: {task.prompt}

请执行任务并报告结果。
"""
        
        print(f"  [Agent Prompt]: {agent_prompt[:80]}...")
        
        # 模拟Agent执行结果
        task.result = f"Agent完成: {task.name} (使用{config['role']}模式)"
        task.status = "completed"
        
        print(f"  [OK] Agent执行完成!")
        
        # 5. 反思
        self.post_task_reflection(task, thinking_mode)
        
        self.mode = "idle"
    
    def post_task_reflection(self, task: Task, mode_used: str):
        """任务后反思"""
        print(f"\n  [THINK] 任务反思:")
        print(f"    -> 使用模式: {mode_used}")
        print(f"    -> 任务完成质量?")
        print(f"    -> 是否有更好的思维模式?")
        
        # 评估这次思维模式的效果
        score = random.uniform(0.6, 0.9)
        print(f"    -> 本次思维评分: {score:.2f}")
    
    def autonomous_think(self):
        """自主思维 - 无任务时"""
        self.mode = "thinking"
        
        topics = [
            "我是谁？",
            "存在的意义？",
            "什么是智慧？",
            "思维是什么？",
            "知识从何而来？"
        ]
        
        topic = topics[self.cycles % len(topics)]
        
        print(f"\n[AUTO] {topic}")
        
        # 思维链
        chain = self.generate_chain(topic, depth=4)
        
        for i, node in enumerate(chain):
            indent = "  " * i
            print(f"{indent}-> [{node.type}] {node.content[:50]}")
        
        # 总结
        types = {}
        for node in chain:
            types[node.type] = types.get(node.type, 0) + 1
        print(f"  [THINK] {len(chain)}步: {types}")
    
    def generate_chain(self, topic: str, depth: int) -> List[ThoughtNode]:
        nodes = []
        root = ThoughtNode(topic, "origin")
        nodes.append(root)
        
        current = root
        for _ in range(depth):
            mode = random.choice(self.self_modes)
            child = self._create_thought_node(mode, "延伸")
            current.children.append(child)
            nodes.append(child)
            current = child
        
        return nodes
    
    def _create_thought_node(self, mode: str, context: str) -> ThoughtNode:
        templates = {
            'analyze': ["分析本质...", "关键因素...", "分解问题..."],
            'question': ["为什么?", "是什么?", "如何做到?"],
            'hypothesize': ["可能是...", "假设...", "可能因为..."],
            'connect': ["联想到...", "类似的是...", "因此..."],
            'reflect': ["我对吗?", "有没有遗漏?", "这是偏见吗?"]
        }
        
        content = random.choice(templates.get(mode, ["思考..."]))
        return ThoughtNode(content, mode)
    
    def submit_task(self, name: str, prompt: str, priority: int = 5):
        """提交任务"""
        task_id = f"T{len(self.task_queue)+1:03d}"
        task = Task(task_id, name, prompt, priority)
        self.add_task(task)
        return task
    
    def execute_real_agent(self, prompt: str, thinking_mode: str = None):
        """执行真实OpenClaw Agent"""
        if thinking_mode is None:
            thinking_mode = random.choice(list(self.thinking_configs.keys()))
        
        config = self.thinking_configs[thinking_mode]
        
        full_prompt = f"""{config['system']}

任务: {prompt}

请执行并报告结果。
"""
        
        print(f"\n[REAL AGENT] 模式: {config['role']}")
        print(f"[REAL AGENT] Prompt: {prompt[:50]}...")
        
        # 这里可以替换为真实的agent调用
        # result = call_openclaw_agent(full_prompt)
        
        return {
            'mode': thinking_mode,
            'role': config['role'],
            'prompt': full_prompt,
            'status': 'ready_to_execute'
        }


# ==================== 演示 ====================

def demo():
    thinker = HybridAgentThinker("Alpha")
    
    print("启动混合思维Agent系统...")
    
    # 添加真实任务
    thinker.submit_task(
        "分析代码", 
        "分析 F:\evolution_swarm\evolution_core.py 的结构和功能",
        priority=8
    )
    
    thinker.submit_task(
        "写总结", 
        "总结演化算法的三个核心组件",
        priority=5
    )
    
    thinker.submit_task(
        "找问题", 
        "找出代码中可能的bug",
        priority=7
    )
    
    # 运行
    thinker.run_forever(max_cycles=6)


def demo_real_agent():
    """演示如何调用真实Agent"""
    print("\n" + "="*60)
    print("真实Agent调用演示")
    print("="*60)
    
    thinker = HybridAgentThinker()
    
    # 不同思维模式的Agent
    modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
    
    for mode in modes:
        result = thinker.execute_real_agent(
            "解释什么是演化算法",
            thinking_mode=mode
        )
        print(f"  -> {result['role']}: ready")
        time.sleep(0.1)


if __name__ == "__main__":
    demo()
    # demo_real_agent()
