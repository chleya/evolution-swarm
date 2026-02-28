# -*- coding: utf-8 -*-
"""
Adaptive Continuum with REAL LLM - 真实LLM驱动的自适应思维
"""

import requests
import random
import time
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime


# ==================== LLM 接口 ====================

class RealLLM:
    """真实LLM接口"""
    
    def __init__(self):
        self.api_key = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"
        self.model = "MiniMax-M2.1"
        self.base_url = "https://api.minimaxi.com/v1"
    
    def chat(self, 
             prompt: str, 
             system: str = None,
             temperature: float = 0.7) -> str:
        """调用真实LLM"""
        
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
                return f"[API Error: {resp.status_code}] {resp.text[:50]}"
        
        except Exception as e:
            return f"[Error: {str(e)}]"


# ==================== 思维系统 ====================

@dataclass
class Thought:
    """思维"""
    id: str
    content: str
    agent_id: str
    agent_type: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AdaptiveLLMSystem:
    """LLM驱动的自适应系统"""
    
    def __init__(self, name: str = "Alpha"):
        self.name = name
        self.llm = RealLLM()
        
        # 思维缓冲
        self.thought_buffer: List[Thought] = []
        self.max_buffer = 20
        
        # 智能体 - 不同思维风格
        self.agents: List[Dict] = [
            {'id': 'analytical', 'name': '分析者', 'system': '你是一个严谨的分析者，擅长逻辑推理。你的回答要简洁、精确。'},
            {'id': 'creative', 'name': '创造者', 'system': '你是一个富有创造力的思考者，擅长联想和创新。'},
            {'id': 'critical', 'name': '批判者', 'system': '你是一个批判性思考者，擅长质疑和分析问题。'},
            {'id': 'systemic', 'name': '系统思考者', 'system': '你是一个系统性思考者，擅长全局视角。'},
            {'id': 'intuitive', 'name': '直觉者', 'system': '你是一个直觉敏锐的思考者，擅长快速洞察。'},
        ]
        
        # 环境
        self.environment = "neutral"
        
        self.thought_count = 0
    
    def set_environment(self, env: str):
        """设置环境"""
        self.environment = env
    
    def generate_thought(self, agent: Dict, context: str) -> Thought:
        """生成思维 - 调用真实LLM"""
        
        # 根据环境构建提示词
        env_prompts = {
            'neutral': f"当前思考上下文: {context}\n\n请自由思考，直接输出你的想法。",
            'crisis': f"当前环境紧迫! 你需要快速分析形势并给出建议。\n\n上下文: {context}",
            'exploration': f"当前环境充满未知和可能性。\n\n上下文: {context}\n\n请提出有趣的探索方向或问题。",
            'calm': f"当前环境平静，是回顾和反思的好时机。\n\n上下文: {context}\n\n请思考如何改进或深化。"
        }
        
        user_prompt = env_prompts.get(self.environment, env_prompts['neutral'])
        
        # 调用LLM
        response = self.llm.chat(
            prompt=user_prompt,
            system=agent['system'],
            temperature=0.7
        )
        
        self.thought_count += 1
        
        thought = Thought(
            id=f"t_{self.thought_count}",
            content=response,
            agent_id=agent['id'],
            agent_type=agent['name']
        )
        
        # 加入缓冲
        self.thought_buffer.append(thought)
        if len(self.thought_buffer) > self.max_buffer:
            self.thought_buffer.pop(0)
        
        return thought
    
    def run_cycle(self) -> List[Thought]:
        """运行一个周期"""
        results = []
        
        # 获取上下文
        if self.thought_buffer:
            context = " | ".join([t.content[:40] for t in self.thought_buffer[-3:]])
        else:
            context = "系统刚刚启动..."
        
        # 每个智能体产生思维
        for agent in self.agents:
            thought = self.generate_thought(agent, context)
            results.append(thought)
            time.sleep(0.3)  # 避免API限流
        
        return results
    
    def run(self, cycles: int = 3):
        """运行多周期"""
        print("\n" + "="*60)
        print(f"{self.name} - REAL LLM Adaptive System")
        print("="*60)
        
        # 环境变化
        envs = ['neutral', 'exploration', 'calm']
        
        for cycle in range(cycles):
            env = envs[cycle % len(envs)]
            self.set_environment(env)
            
            print(f"\n{'='*60}")
            print(f"[Cycle {cycle+1}] Environment: {env}")
            print("="*60)
            
            # 生成思维
            thoughts = self.run_cycle()
            
            # 打印
            for t in thoughts:
                content = t.content[:80] + "..." if len(t.content) > 80 else t.content
                print(f"\n[{t.agent_type}]")
                print(f"  {content}")
            
            print(f"\n{'─'*40}")
        
        print("\n" + "="*60)
        print("System Complete")
        print("="*60)
        
        # 总结
        print(f"\nTotal Thoughts: {len(self.thought_buffer)}")
        
        # 按智能体统计
        agent_counts = {}
        for t in self.thought_buffer:
            agent_counts[t.agent_type] = agent_counts.get(t.agent_type, 0) + 1
        
        print("\nThoughts by Agent:")
        for agent_id, count in agent_counts.items():
            print(f"  {agent_id}: {count}")


# ==================== 演示 ====================

def demo():
    """演示"""
    print("\n" + "="*60)
    print("LLM-POWERED ADAPTIVE THINKING - WITH REAL API")
    print("="*60)
    
    system = AdaptiveLLMSystem("Alpha")
    system.run(cycles=2)


if __name__ == "__main__":
    demo()
