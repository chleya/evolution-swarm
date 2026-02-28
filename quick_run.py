# -*- coding: utf-8 -*-
"""
Continuum Quick Run - 快速运行版
"""

import requests
import time
import random

API_KEY = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"

def llm_chat(prompt, system):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "MiniMax-M2.1",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        resp = requests.post("https://api.minimaxi.com/v1/text/chatcompletion_v2",
            headers=headers, json=data, timeout=25)
        
        if resp.status_code == 200:
            result = resp.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {resp.status_code}"
    except Exception as e:
        return f"Exception: {str(e)[:30]}"


def run():
    print("\n" + "="*60)
    print("CONTINUUM SYSTEM - Running")
    print("="*60)
    
    agents = [
        ("分析者", "你是一个严谨的分析者，简洁有力。"),
        ("创造者", "你是一个有创造力的思考者。"),
        ("批判者", "你是一个批判性思考者。"),
    ]
    
    topics = [
        "AI的未来",
        "什么是意识",
        "如何创新",
    ]
    
    for gen in range(3):
        print(f"\n{'='*60}")
        print(f"Generation {gen+1}")
        print("="*60)
        
        topic = topics[gen % len(topics)]
        print(f"\n[Topic] {topic}\n")
        
        for name, system in agents:
            print(f"[{name}]")
            
            prompt = f"关于'{topic}'，用30字以内说出你的想法。"
            response = llm_chat(prompt, system)
            
            print(f"  {response[:80]}")
            time.sleep(0.5)
    
    print("\n" + "="*60)
    print("Complete!")
    print("="*60)


if __name__ == "__main__":
    run()
