# -*- coding: utf-8 -*-
"""
LLM Integration - 大语言模型思维生成
"""

import os
import json
from typing import List, Dict, Optional


class LLMThinker:
    """LLM思维生成器"""
    
    def __init__(self, model: str = "minimax/MiniMax-M2.1"):
        self.model = model
        self.api_key = os.environ.get("MINIMAX_API_KEY", "")
        self.base_url = "https://api.minimax.chat/v1"
    
    def think(self, 
              prompt: str, 
              system_prompt: str = None,
              temperature: float = 0.7) -> str:
        """调用LLM生成思维"""
        
        if not self.api_key:
            return self._fallback_think(prompt)
        
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/text/chatcompletion_v2",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"[API Error: {response.status_code}]"
        
        except Exception as e:
            return f"[Error: {str(e)}]"
    
    def _fallback_think(self, prompt: str) -> str:
        """备用生成"""
        thoughts = [
            "这是一个值得深思的问题...",
            "让我从多个角度分析...",
            "根据当前信息，我推测...",
            "这可能涉及到...",
            "需要进一步探索...",
        ]
        return f"[模拟] {prompt[:30]}... {hash(prompt) % 100}"


class HybridLLMThinker:
    """混合思维 - LLM + 模板"""
    
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.llm = LLMThinker() if use_llm else None
        
        # 模板作为后备
        self.templates = {
            'drift': [
                "这让我联想到...",
                "也许可以从另一个角度看...",
                "有没有可能...",
                "突然想到..."
            ],
            'focus': [
                "分析这个问题...",
                "首先...",
                "因此...",
                "结论是..."
            ],
            'integrate': [
                "回顾一下...",
                "总结经验...",
                "接下来...",
                "还可以..."
            ]
        }
    
    def generate(self, 
                 mode: str, 
                 context: str,
                 topic: str = None) -> str:
        """生成思维"""
        
        if self.use_llm and self.llm and self.llm.api_key:
            # 使用LLM
            system_prompts = {
                'drift': "你是一个自由思考者，允许联想自由飞翔，接受意外的思维跳转。",
                'focus': "你是一个专注的思考者，保持逻辑严密，专注于当前问题。",
                'integrate': "你是一个整合者，回顾思考，将其与宏观主题联系。"
            }
            
            prompt = f"""当前思维上下文:
{context}

请基于以上内容，继续思考。直接给出你的想法，不需要格式。"""
            
            return self.llm.think(
                prompt=prompt,
                system_prompt=system_prompts.get(mode, "你是一个思考者。")
            )
        else:
            # 使用模板
            template = random.choice(self.templates.get(mode, ['思考中...']))
            return f"{template} {context[:30]}..."


# 测试
def test_llm():
    """测试LLM"""
    print("\n" + "="*50)
    print("LLM Thinking Test")
    print("="*50)
    
    thinker = HybridLLMThinker(use_llm=True)
    
    # 测试生成
    modes = ['drift', 'focus', 'integrate']
    
    for mode in modes:
        print(f"\n[{mode.upper()}]")
        result = thinker.generate(
            mode=mode,
            context="刚才在思考人工智能的未来...",
            topic="意识"
        )
        print(f"Result: {result[:100]}...")


if __name__ == "__main__":
    import random
    test_llm()
