# -*- coding: utf-8 -*-
"""
Minimal LLM Test - 最简LLM测试
"""

import requests

API_KEY = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"

def think(topic):
    print(f"\n=== Thinking about: {topic} ===")
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    data = {
        "model": "MiniMax-M2.1",
        "messages": [{"role": "user", "content": f"关于'{topic}'，请用50字以内说出你的想法。"}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    resp = requests.post("https://api.minimaxi.com/v1/text/chatcompletion_v2",
        headers=headers, json=data, timeout=20)
    
    if resp.status_code == 200:
        content = resp.json()['choices'][0]['message']['content']
        print(f"[Thought] {content}")
        return content
    else:
        print(f"[Error] {resp.status_code}")
        return None

print("="*50)
print("REAL LLM THINKING TEST")
print("="*50)

topics = ["AI的未来", "什么是意识", "如何创新"]

for t in topics:
    think(t)

print("\nDone!")
