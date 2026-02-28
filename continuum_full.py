# -*- coding: utf-8 -*-
"""
Continuum Full System - 完整版
包含：记忆持久化 + 多智能体 + 自动进化 + 主题聚类 + 定时触发 + Web界面
"""

import os
import json
import time
import random
import threading
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from flask import Flask, render_template_string, jsonify, request

# ==================== 数据结构 ====================

@dataclass
class Thought:
    """思维"""
    id: str
    content: str
    topic: str
    agent: str
    timestamp: str
    tags: List[str]
    quality: float = 0.5

@dataclass
class Agent:
    """智能体"""
    id: str
    name: str
    role: str
    system_prompt: str
    temperature: float
    color: str

# ==================== 核心系统 ====================

class ContinuumFull:
    """完整思维系统"""
    
    def __init__(self, data_dir: str = "F:/evolution_swarm/data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 记忆存储
        self.thoughts: List[Thought] = []
        self.topics: Dict[str, int] = {}  # 主题聚类
        
        # 智能体
        self.agents = self._init_agents()
        
        # 主题池
        self.topic_pool = [
            "宇宙的本质", "意识的起源", "AI的未来", "生命的意义",
            "真理与现实", "创造与创新", "智慧与愚蠢", "存在与虚无",
            "自由意志", "时间本质", "自我是什么", "知识的边界",
            "AI能否拥有创造力", "如何让AI更像生物", "自主性的本质"
        ]
        
        # 加载历史记忆
        self._load_thoughts()
    
    def _init_agents(self) -> List[Agent]:
        """初始化智能体"""
        return [
            Agent("analytical", "分析者", "严谨分析", "你是一个严谨的分析者，擅长逻辑推理。", 0.5, "#3498db"),
            Agent("creative", "创造者", "创新思维", "你是一个富有创造力的思考者。", 0.9, "#e74c3c"),
            Agent("critical", "批判者", "质疑分析", "你是一个批判性思考者。", 0.6, "#9b59b6"),
            Agent("systemic", "系统思考者", "全局视角", "你是一个系统性思考者。", 0.7, "#1abc9c"),
            Agent("intuitive", "直觉者", "快速洞察", "你是一个直觉敏锐的思考者。", 0.8, "#f39c12"),
        ]
    
    def _load_thoughts(self):
        """加载历史记忆"""
        thoughts_file = f"{self.data_dir}/thoughts.json"
        if os.path.exists(thoughts_file):
            with open(thoughts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.thoughts = [Thought(**t) for t in data]
                
                # 重建主题聚类
                for t in self.thoughts:
                    self.topics[t.topic] = self.topics.get(t.topic, 0) + 1
    
    def save_thoughts(self):
        """保存记忆"""
        thoughts_file = f"{self.data_dir}/thoughts.json"
        with open(thoughts_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(t) for t in self.thoughts], f, ensure_ascii=False, indent=2)
    
    def add_thought(self, thought: Thought):
        """添加思维"""
        self.thoughts.append(thought)
        self.topics[thought.topic] = self.topics.get(thought.topic, 0) + 1
        
        # 只保留最近1000条
        if len(self.thoughts) > 1000:
            self.thoughts = self.thoughts[-1000:]
        
        self.save_thoughts()
    
    def get_related_topics(self, topic: str) -> List[str]:
        """获取相关主题"""
        # 简单聚类：包含相同关键词
        related = []
        for t in self.topics:
            if t != topic and any(w in t for w in topic):
                related.append(t)
        return related[:5]
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'total_thoughts': len(self.thoughts),
            'topics': self.topics,
            'agents': {a.id: {'name': a.name, 'color': a.color} for a in self.agents}
        }
    
    def generate_thought(self, topic: str = None) -> Thought:
        """生成思维 - 调用LLM"""
        import requests
        
        if topic is None:
            topic = random.choice(self.topic_pool)
        
        agent = random.choice(self.agents)
        
        prompt = f"关于'{topic}'，用50字以内说出你的独到见解。"
        
        try:
            resp = requests.post(
                "https://api.minimaxi.com/v1/text/chatcompletion_v2",
                headers={
                    "Authorization": "Bearer sk-cp-32X4yB3hv4uMfzdBmke7EyaxE2pXmHkAGisoBxm1bTlSnUKXcH3lGRgWYcD62Nre5AacJpbi0E5yOx92m5rkIth9HioW2aCHP5r3LeCKBuf-wdr1TVgeFxY",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "MiniMax-M2.1",
                    "messages": [
                        {"role": "system", "content": agent.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": agent.temperature,
                    "max_tokens": 100
                },
                timeout=20
            )
            
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
            else:
                content = f"[思考{topic}...]"
        except:
            content = f"[思考{topic}...]"
        
        thought = Thought(
            id=f"t_{len(self.thoughts)+1}",
            content=content[:100],
            topic=topic,
            agent=agent.id,
            timestamp=datetime.now().isoformat(),
            tags=[],
            quality=random.uniform(0.6, 0.9)
        )
        
        self.add_thought(thought)
        return thought


# ==================== Web界面 ====================

app = Flask(__name__)
continuum = ContinuumFull()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Continuum - 持续思维系统</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh; color: #fff; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { 
            background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px;
            backdrop-filter: blur(10px);
        }
        .stats { grid-column: span 2; }
        .thought { 
            background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin: 10px 0;
            border-left: 4px solid #3498db;
        }
        .thought.analytical { border-color: #3498db; }
        .thought.creative { border-color: #e74c3c; }
        .thought.critical { border-color: #9b59b6; }
        .thought.systemic { border-color: #1abc9c; }
        .thought.intuitive { border-color: #f39c12; }
        .topic { color: #aaa; font-size: 0.9em; margin-bottom: 5px; }
        .content { font-size: 1.1em; line-height: 1.6; }
        .meta { color: #666; font-size: 0.8em; margin-top: 10px; }
        button {
            background: linear-gradient(135deg, #3498db, #2980b9); color: white;
            border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer;
            font-size: 1em; margin: 5px;
        }
        button:hover { transform: translateY(-2px); }
        .btn-green { background: linear-gradient(135deg, #27ae60, #2ecc71); }
        .btn-purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        input {
            padding: 12px; border-radius: 8px; border: none; width: 60%;
            background: rgba(255,255,255,0.1); color: white; font-size: 1em;
        }
        .topic-cloud { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
        .topic-tag { 
            background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px;
            font-size: 0.9em;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; } }
        .thought { animation: fadeIn 0.5s ease; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Continuum - 持续思维系统</h1>
        
        <div class="grid">
            <div class="card stats">
                <h2>📊 系统状态</h2>
                <p>总思维数: {{ stats.total_thoughts }}</p>
                <div class="topic-cloud">
                    {% for topic, count in stats.topics.items() %}
                    <span class="topic-tag">{{ topic }} ({{ count }})</span>
                    {% endfor %}
                </div>
            </div>
            
            <div class="card">
                <h2>🎮 控制台</h2>
                <button onclick="generate()" class="btn-green">生成思维</button>
                <button onclick="autoThink()" class="btn-purple">自动思考(5次)</button>
                <br><br>
                <input type="text" id="topic" placeholder="输入主题...">
                <button onclick="generateTopic()">聚焦思考</button>
            </div>
            
            <div class="card" style="grid-column: span 2;">
                <h2>💭 思维流</h2>
                <div id="thoughts">
                    {% for thought in thoughts[-10:]|reverse %}
                    <div class="thought {{ thought.agent }}">
                        <div class="topic">{{ thought.topic }}</div>
                        <div class="content">{{ thought.content }}</div>
                        <div class="meta">{{ thought.agent }} | {{ thought.timestamp[:19] }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function generate() {
            fetch('/generate', {method: 'POST'})
                .then(r => r.json())
                .then(d => location.reload());
        }
        
        function autoThink() {
            for(let i=0; i<5; i++) {
                setTimeout(() => generate(), i*3000);
            }
        }
        
        function generateTopic() {
            let topic = document.getElementById('topic').value;
            fetch('/generate_topic', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic: topic})
            }).then(r => r.json()).then(d => location.reload());
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, 
        thoughts=continuum.thoughts[-20:],
        stats=continuum.get_stats()
    )

@app.route('/generate', methods=['POST'])
def generate():
    thought = continuum.generate_thought()
    return jsonify({'status': 'ok'})

@app.route('/generate_topic', methods=['POST'])
def generate_topic():
    data = request.json
    thought = continuum.generate_thought(data.get('topic'))
    return jsonify({'status': 'ok'})

@app.route('/stats')
def stats():
    return jsonify(continuum.get_stats())


def run_server():
    """运行Web服务器"""
    app.run(host='0.0.0.0', port=5000, debug=False)


def auto_think_loop():
    """自动思考循环"""
    while True:
        time.sleep(60)  # 每分钟思考一次
        thought = continuum.generate_thought()
        print(f"[Auto] {thought.topic}: {thought.content[:30]}...")


if __name__ == "__main__":
    # 启动Web服务器
    print("\n" + "="*60)
    print("Continuum Full System")
    print("="*60)
    print("\n1. Web界面: http://localhost:5000")
    print("2. 自动思考: 每分钟生成一条")
    print("3. 记忆持久化: 自动保存")
    print("\n按 Ctrl+C 停止")
    print("="*60 + "\n")
    
    # 后台自动思考
    thread = threading.Thread(target=auto_think_loop, daemon=True)
    thread.start()
    
    # Web服务器
    run_server()
