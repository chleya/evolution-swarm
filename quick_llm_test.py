# -*- coding: utf-8 -*-
"""
Quick LLM Test - 快速LLM测试
"""

import requests

API_KEY = "sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY"
MODEL = "MiniMax-M2.1"

def test_llm():
    print("Testing LLM API...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "你好，请用一句话介绍自己"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        resp = requests.post(
            "https://api.minimaxi.com/v1/text/chatcompletion_v2",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            result = resp.json()
            content = result['choices'][0]['message']['content']
            print(f"Response: {content}")
            return True
        else:
            print(f"Error: {resp.text[:200]}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_llm()
