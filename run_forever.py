# -*- coding: utf-8 -*-
"""
Continuum Forever - 永动思维链
持续运行，直到手动停止
"""

import requests
import time
import random

API_KEY = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"

def llm_chat(prompt, system, temperature=0.7):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "MiniMax-M2.1",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 150
    }
    
    try:
        resp = requests.post("https://api.minimaxi.com/v1/text/chatcompletion_v2",
            headers=headers, json=data, timeout=25)
        
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
        else:
            return f"[Error: {resp.status_code}]"
    except Exception as e:
        return f"[Error: {str(e)[:30]}]"


def run_forever():
    print("\n" + "="*70)
    print("  CONTINUUM FOREVER - 永动思维链")
    print("  按 Ctrl+C 停止")
    print("="*70)
    
    # 智能体
    agents = [
        ("分析者", "你是一个严谨的分析者，擅长逻辑推理。回答要简洁有力。", 0.5),
        ("创造者", "你是一个富有创造力的思考者，擅长联想和创新。", 0.9),
        ("批判者", "你是一个批判性思考者，擅长质疑和分析。", 0.6),
        ("系统思考者", "你是一个系统性思考者，擅长全局视角。", 0.7),
        ("直觉者", "你是一个直觉敏锐的思考者，擅长快速洞察。", 0.8),
    ]
    
    # 主题池
    topics_pool = [
        "宇宙的尽头有什么？",
        "意识的本质是什么？",
        "AI能否拥有创造力？",
        "生命的定义是什么？",
        "时间的本质是什么？",
        "如何让AI更像生物？",
        "智能的极限在哪里？",
        "真理存在吗？",
        "自由意志是否存在？",
        "宇宙是设计的还是随机的？",
        "如何突破人类认知边界？",
        "AI与人类的关系未来会怎样？",
        "什么是真正的智慧？",
        "记忆的本质是什么？",
        "自我是什么？",
    ]
    
    cycle = 0
    
    try:
        while True:
            cycle += 1
            
            # 选择主题
            topic = random.choice(topics_pool)
            
            # 选择智能体
            name, system, temp = random.choice(agents)
            
            print(f"\n{'='*70}")
            print(f"[Cycle {cycle}] {topic}")
            print("-"*70)
            
            # 生成思考
            prompt = f"关于'{topic}'，用50字以内说出你的独到见解。"
            response = llm_chat(prompt, system, temp)
            
            print(f"[{name}]")
            print(f"  {response}")
            
            # 短暂休息
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("  系统已停止")
        print(f"  共运行 {cycle} 个思维周期")
        print("="*70)


if __name__ == "__main__":
    run_forever()
