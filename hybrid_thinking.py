# -*- coding: utf-8 -*-
"""
Hybrid Thinking System - 任务驱动 + 自主思维
有任务时执行任务，无任务时自主思考
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
    def __init__(self, id: str, name: str, priority: int = 5):
        self.id = id
        self.name = name
        self.priority = priority
        self.status = "pending"
        self.result = None


class HybridThinker:
    def __init__(self, name: str = "Thinker"):
        self.name = name
        self.thought_tree = None
        self.task_queue: List[Task] = []
        self.mode = "idle"
        self.cycles = 0
        self.self_modes = ['analyze', 'question', 'hypothesize', 'connect', 'reflect']
    
    def run_forever(self, max_cycles: int = 10):
        print(f"\n{'='*60}")
        print(f"{self.name} 启动 - 任务驱动 + 自主思维")
        print(f"{'='*60}\n")
        
        while self.cycles < max_cycles:
            self.cycles += 1
            
            if self.task_queue:
                task = self.get_next_task()
                self.execute_task(task)
            else:
                self.autonomous_think()
            
            time.sleep(0.2)
        
        print(f"\n停止，共 {self.cycles} 轮")
    
    def get_next_task(self) -> Task:
        self.task_queue.sort(key=lambda t: -t.priority)
        task = self.task_queue.pop(0)
        task.status = "running"
        return task
    
    def add_task(self, task: Task):
        self.task_queue.append(task)
        print(f"\n[TASK] {task.name} (priority: {task.priority})")
    
    def execute_task(self, task: Task):
        self.mode = "tasking"
        
        print(f"\n{'-'*40}")
        print(f"[EXEC] {task.name}")
        print(f"{'-'*40}")
        
        print(f"  -> 理解任务...")
        print(f"  -> 分析任务...")
        print(f"  -> 制定计划...")
        print(f"  -> 执行中...")
        
        task.result = f"Done: {task.name}"
        task.status = "completed"
        
        print(f"  [OK] 完成!")
        
        self.post_task_reflection(task)
        
        self.mode = "idle"
    
    def post_task_reflection(self, task: Task):
        print(f"\n  [THINK] 任务反思:")
        reflections = [
            "任务完成得如何？",
            "有没有更好的方式？",
            "学到了什么？"
        ]
        for r in reflections[:2]:
            print(f"    -> {r}")
    
    def autonomous_think(self):
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
        
        chain = self.generate_chain(topic, depth=3)
        
        for i, node in enumerate(chain):
            indent = "  " * i
            print(f"{indent}-> [{node.type}] {node.content[:40]}")
        
        self.think_summary(chain)
    
    def generate_chain(self, topic: str, depth: int) -> List[ThoughtNode]:
        nodes = []
        root = ThoughtNode(topic, "origin")
        nodes.append(root)
        
        current = root
        for i in range(depth):
            mode = random.choice(self.self_modes)
            child = self._create_thought(mode, current.content)
            current.children.append(child)
            nodes.append(child)
            current = child
        
        return nodes
    
    def _create_thought(self, mode: str, parent_content: str) -> ThoughtNode:
        templates = {
            'analyze': ["这让我想到...", "本质是...", "关键是...", "分解为..."],
            'question': ["为什么？", "是什么？", "如何做到？", "然后呢？"],
            'hypothesize': ["可能是...", "也许...", "假设...", "可能因为..."],
            'connect': ["类似于...", "相反的是...", "同时...", "因此..."],
            'reflect': ["我对吗？", "有没有遗漏？", "还能更深入吗？", "这是偏见吗？"]
        }
        
        content = random.choice(templates.get(mode, ["思考..."]))
        return ThoughtNode(content, mode)
    
    def think_summary(self, chain: List[ThoughtNode]):
        types = {}
        for node in chain:
            types[node.type] = types.get(node.type, 0) + 1
        print(f"  [THINK] {len(chain)}步: {types}")
    
    def submit_task(self, name: str, priority: int = 5):
        task_id = f"T{len(self.task_queue)+1:03d}"
        task = Task(task_id, name, priority)
        self.add_task(task)
        return task


def demo():
    thinker = HybridThinker("Alpha")
    
    print("启动混合思维系统...")
    
    thinker.submit_task("分析数据", priority=8)
    thinker.submit_task("写报告", priority=5)
    thinker.submit_task("优化算法", priority=7)
    
    thinker.run_forever(max_cycles=8)


if __name__ == "__main__":
    demo()
