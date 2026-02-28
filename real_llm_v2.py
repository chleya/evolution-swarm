# -*- coding: utf-8 -*-
"""
Adaptive Continuum with REAL LLM - 真实LLM
"""

import requests
import random
import time
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime


class RealLLM:
    """真实LLM"""
    
    def __init__(self):
        self.api_key = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"
        self.model = "MiniMax-M2.1"
        self.base_url = "https://api.minimaxi.com/v1"
    
    def chat(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
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
            "max_tokens": 200
        }
        
        try:
            resp = requests.post(f"{self.base_url}/text/chatcompletion_v2",
                headers=headers, json=data, timeout=30)
            
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"[Error {resp.status_code}]"
        except Exception as e:
            return f"[Exception: {e}]"


class AdaptiveLLMSystem:
    """自适应LLM系统"""
    
    def __init__(self):
        self.llm = RealLLM()
        self.thoughts = []
        self.agents = [
            {'id': 'analytical', 'name': '分析者', 'system': '你是一个严谨的分析者。'},
            {'id': 'creative', 'name': '创造者', 'system': '你是一个有创造力的思考者。'},
            {'id': 'critical', 'name': '批判者', 'system': '你是一个批判性思考者。'},
        ]
    
    def think(self, topic: str) -> List[Dict]:
        """让每个智能体思考"""
        results = []
        
        for agent in self.agents:
            prompt = f"主题: {topic}\n\n请直接说出你的想法，不要格式。"
            
            response = self.llm.chat(prompt, agent['system'])
            
            results.append({
                'agent': agent['name'],
                'thought': response[:100]
            })
            
            time.sleep(0.5)
        
        return results
    
    def run(self):
        print("\n" + "="*60)
        print("ADAPTIVE LLM SYSTEM - WITH REAL API")
        print("="*60)
        
        topics = [
            "人工智能的未来",
            "如何让AI更像生物",
            "意识的本质"
        ]
        
        for topic in topics:
            print(f"\n[Topic: {topic}]")
            print("-" * 40)
            
            results = self.think(topic)
            
            for r in results:
                print(f"\n[{r['agent']}]")
                print(f"  {r['thought']}")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    system = AdaptiveLLMSystem()
    system.run()
