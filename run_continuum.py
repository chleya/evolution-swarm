# -*- coding: utf-8 -*-
"""
Continuum Running - 持续思维链运行中
结合所有组件：适应 + LLM思考 + 演化
"""

import os
import sys
import time
import requests
import random
from datetime import datetime

# API配置
API_KEY = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"
MODEL = "MiniMax-M2.1"

# ==================== 核心组件 ====================

class Agent:
    """智能体"""
    def __init__(self, id, name, role, system_prompt):
        self.id = id
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.thoughts = []
        self.fitness = 0.5
    
    def think(self, topic, llm):
        """思考"""
        prompt = f"主题: {topic}\n\n直接说出你的想法，简洁有力。"
        response = llm.chat(prompt, self.system_prompt)
        self.thoughts.append(response)
        
        # 适应度更新
        self.fitness = min(1.0, self.fitness + 0.05)
        
        return response


class LLM:
    """LLM接口"""
    def __init__(self):
        self.api_key = API_KEY
        self.model = MODEL
    
    def chat(self, prompt, system=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            resp = requests.post(
                "https://api.minimaxi.com/v1/text/chatcompletion_v2",
                headers=headers, json=data, timeout=30
            )
            
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"[API错误: {resp.status_code}]"
        except Exception as e:
            return f"[异常: {str(e)[:30]}]"


class Environment:
    """环境"""
    def __init__(self, name, pressure, topics):
        self.name = name
        self.pressure = pressure
        self.topics = topics


# ==================== 主系统 ====================

class ContinuumSystem:
    """持续思维系统"""
    
    def __init__(self):
        self.llm = LLM()
        self.agents = []
        self.thought_history = []
        self.generation = 0
        self.running = False
        
        # 初始化智能体
        self._init_agents()
        
        # 环境列表
        self.environments = [
            Environment("探索模式", "curiosity", [
                "宇宙的尽头是什么？",
                "意识的起源",
                "AI能否有创造力",
                "生命的定义",
                "时间是什么？"
            ]),
            Environment("分析模式", "logic", [
                "如何优化这个系统？",
                "数据的本质",
                "算法的极限",
                "计算的意义",
                "模型能做什么？"
            ]),
            Environment("创造模式", "creative", [
                "如何发明新东西？",
                "艺术的本质",
                "创新的来源",
                "想象力的边界",
                "如何突破常规？"
            ]),
            Environment("整合模式", "integrate", [
                "如何把所有知识联系起来？",
                "统一的理论",
                "万物的规律",
                "如何理解复杂性？",
                "系统的本质"
            ])
        ]
        
        self.current_env = self.environments[0]
    
    def _init_agents(self):
        """初始化智能体"""
        agents_data = [
            ("analytical", "分析者", "你是一个严谨的分析者，擅长逻辑推理。你的回答要简洁、深刻。"),
            ("creative", "创造者", "你是一个富有创造力的思考者，擅长联想和创新。"),
            ("critical", "批判者", "你是一个批判性思考者，擅长质疑和分析问题。"),
            ("systemic", "系统思考者", "你是一个系统性思考者，擅长全局视角和关系分析。"),
            ("intuitive", "直觉者", "你是一个直觉敏锐的思考者，擅长快速洞察本质。"),
        ]
        
        for i, (id, name, prompt) in enumerate(agents_data):
            self.agents.append(Agent(f"agent_{i}", name, id, prompt))
        
        print(f"[Init] Created {len(self.agents)} agents")
    
    def evolve(self):
        """演化一代"""
        self.generation += 1
        
        # 按适应度排序
        self.agents.sort(key=lambda a: a.fitness, reverse=True)
        
        # 精英保留
        elite = self.agents[:2]
        
        # 打印状态
        print(f"\n{'='*70}")
        print(f"Generation {self.generation} | Environment: {self.current_env.name}")
        print(f"{'='*70}")
        
        # 环境切换
        self.current_env = self.environments[self.generation % len(self.environments)]
        
        # 选择主题
        topic = random.choice(self.current_env.topics)
        
        print(f"\n[Topic] {topic}")
        print("-" * 50)
        
        # 每个智能体思考
        for agent in self.agents:
            print(f"\n[{agent.name}]")
            
            thought = agent.think(topic, self.llm)
            
            # 打印思考
            lines = thought.split('\n')[:3]
            for line in lines:
                print(f"  {line[:80]}")
            
            self.thought_history.append({
                'agent': agent.name,
                'thought': thought[:100],
                'generation': self.generation
            })
            
            time.sleep(0.5)
        
        # 适应度自然衰减（模拟遗忘）
        for agent in self.agents:
            agent.fitness = max(0.3, agent.fitness * 0.95)
        
        # 打印统计
        print(f"\n{'─'*50}")
        print(f"Stats: Generation={self.generation}, Thoughts={len(self.thought_history)}")
        
        best = max(self.agents, key=lambda a: a.fitness)
        print(f"Best Agent: {best.name} (fitness: {best.fitness:.2f})")
    
    def run(self, generations=10):
        """运行"""
        self.running = True
        
        print("\n" + "="*70)
        print("  CONTINUUM SYSTEM - Running with Real LLM")
        print("="*70)
        
        for i in range(generations):
            self.evolve()
            
            if i < generations - 1:
                print("\n[Thinking...]")
                time.sleep(1)
        
        print("\n" + "="*70)
        print("  SYSTEM HALTED")
        print("="*70)
        
        # 最终报告
        print("\n" + "="*70)
        print("  FINAL REPORT")
        print("="*70)
        
        print(f"\nTotal Generations: {self.generation}")
        print(f"Total Thoughts: {len(self.thought_history)}")
        
        print("\nAgent Performance:")
        for agent in sorted(self.agents, key=lambda a: -a.fitness):
            print(f"  {agent.name}: fitness={agent.fitness:.2f}, thoughts={len(agent.thoughts)}")
        
        print("\nRecent Thoughts:")
        for t in self.thought_history[-5:]:
            print(f"  [{t['agent']}] {t['thought'][:60]}...")


# ==================== 运行 ====================

if __name__ == "__main__":
    print("Starting Continuum System...")
    
    system = ContinuumSystem()
    system.run(generations=6)
