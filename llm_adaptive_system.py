# -*- coding: utf-8 -*-
"""
Adaptive Continuum with LLM - 真实LLM驱动的自适应思维
"""

import os
import random
import time
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ==================== LLM 接口 ====================

class LLMInterface:
    """LLM接口"""
    
    def __init__(self):
        self.api_key = os.environ.get("MINIMAX_API_KEY", "")
        self.model = "minimax/MiniMax-M2.1"
        self.base_url = "https://api.minimax.chat/v1"
    
    def chat(self, 
             prompt: str, 
             system: str = None,
             temperature: float = 0.7) -> str:
        """对话"""
        
        if not self.api_key:
            return self._mock_response(prompt)
        
        import requests
        
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
            "temperature": temperature,
            "max_tokens": 300
        }
        
        try:
            resp = requests.post(
                f"{self.base_url}/text/chatcompletion_v2",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if resp.status_code == 200:
                result = resp.json()
                return result['choices'][0]['message']['content']
            else:
                return self._mock_response(prompt)
        
        except Exception as e:
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """模拟响应"""
        responses = [
            "这是一个有趣的想法...",
            "让我思考一下...",
            "根据我的分析...",
            "或许我们可以...",
            "这让我联想到..."
        ]
        return f"[思考] {random.choice(responses)} {prompt[:20]}..."


# ==================== 思维系统 ====================

@dataclass
class Thought:
    """思维"""
    id: str
    content: str
    agent_id: str
    mode: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AdaptiveLLMSystem:
    """LLM驱动的自适应系统"""
    
    def __init__(self, name: str = "Alpha"):
        self.name = name
        self.llm = LLMInterface()
        
        # 思维缓冲
        self.thought_buffer: List[Thought] = []
        self.max_buffer = 20
        
        # 智能体
        self.agents: List[Dict] = []
        self._init_agents(5)
        
        # 环境
        self.environment = "neutral"
        
        # 运行状态
        self.running = False
    
    def _init_agents(self, count: int):
        """初始化智能体"""
        for i in range(count):
            self.agents.append({
                'id': f'agent_{i}',
                'name': f'Agent-{i+1}',
                'mode': random.choice(['analytical', 'creative', 'critical']),
                'personality': random.choice(['curious', 'cautious', 'bold', 'balanced'])
            })
    
    def set_environment(self, env: str):
        """设置环境"""
        self.environment = env
    
    def generate_thought(self, agent: Dict, context: str) -> Thought:
        """生成思维 - 调用LLM"""
        
        # 构建提示词
        system_prompts = {
            'analytical': "你是一个严谨的分析者，擅长逻辑推理。",
            'creative': "你是一个富有创造力的思考者，擅长联想创新。",
            'critical': "你是一个批判性思考者，擅长质疑和分析。"
        }
        
        user_prompts = {
            'neutral': f"当前上下文: {context}\n\n请自由思考，输出你的想法。",
            'crisis': f"当前环境紧迫: {self.environment}\n\n请快速分析形势并给出建议。",
            'exploration': f"当前环境充满未知: {self.environment}\n\n请提出有趣的探索方向。",
            'calm': f"当前环境平静。\n\n请回顾过去，思考如何改进。"
        }
        
        system = system_prompts.get(agent['mode'], "你是一个思考者。")
        user = user_prompts.get(self.environment, user_prompts['neutral'])
        
        # 调用LLM
        response = self.llm.chat(
            prompt=user,
            system=system,
            temperature=0.7
        )
        
        thought = Thought(
            id=f"thought_{len(self.thought_buffer)}",
            content=response,
            agent_id=agent['id'],
            mode=agent['mode']
        )
        
        # 加入缓冲
        self.thought_buffer.append(thought)
        if len(self.thought_buffer) > self.max_buffer:
            self.thought_buffer.pop(0)
        
        return thought
    
    def run_cycle(self, num_thoughts: int = 3) -> List[Thought]:
        """运行一个周期"""
        results = []
        
        # 获取上下文
        if self.thought_buffer:
            context = " | ".join([t.content[:50] for t in self.thought_buffer[-3:]])
        else:
            context = "系统刚刚启动..."
        
        # 每个智能体产生思维
        for _ in range(num_thoughts):
            agent = random.choice(self.agents)
            thought = self.generate_thought(agent, context)
            results.append(thought)
        
        return results
    
    def run(self, cycles: int = 10):
        """运行多周期"""
        self.running = True
        
        print("\n" + "="*60)
        print(f"{self.name} - LLM-Driven Adaptive System")
        print("="*60)
        
        # 环境变化
        envs = ['neutral', 'crisis', 'exploration', 'calm']
        
        for cycle in range(cycles):
            env = envs[cycle % len(envs)]
            self.set_environment(env)
            
            # 生成思维
            thoughts = self.run_cycle(num_thoughts=3)
            
            # 打印
            print(f"\n[Cycle {cycle+1}] Environment: {env}")
            
            for t in thoughts:
                content = t.content[:60] + "..." if len(t.content) > 60 else t.content
                print(f"  [{t.agent_id}:{t.mode}] {content}")
            
            time.sleep(0.5)
        
        print("\n" + "="*60)
        print("System Halted")
        print("="*60)
        
        # 总结
        print(f"\nTotal Thoughts: {len(self.thought_buffer)}")
        
        # 按智能体统计
        agent_counts = {}
        for t in self.thought_buffer:
            agent_counts[t.agent_id] = agent_counts.get(t.agent_id, 0) + 1
        
        print("\nThoughts by Agent:")
        for agent_id, count in agent_counts.items():
            print(f"  {agent_id}: {count}")


# ==================== 演示 ====================

def demo():
    """演示"""
    print("\n" + "="*60)
    print("LLM-POWERED ADAPTIVE THINKING SYSTEM")
    print("="*60)
    
    # 检查API
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if api_key:
        print(f"[OK] Using LLM API")
    else:
        print(f"[Note] No API key, using mock responses")
    
    system = AdaptiveLLMSystem("Alpha")
    system.run(cycles=8)


if __name__ == "__main__":
    demo()
