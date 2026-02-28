# -*- coding: utf-8 -*-
"""
Evolutionary Intelligence Swarm - OpenClaw Integration
演化智能群 - OpenClaw集成层
"""

import json
import os
from typing import Dict, List, Optional


class OpenClawIntegrator:
    """OpenClaw集成器"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace = workspace_path or "F:/evolution_swarm"
        self.population_dir = f"{self.workspace}/population"
        self.ensure_dirs()
    
    def ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(self.population_dir, exist_ok=True)
    
    def save_variant(self, variant: Dict):
        """保存变体到文件"""
        variant_id = variant['variant_id']
        filepath = f"{self.population_dir}/{variant_id}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(variant, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_variant(self, variant_id: str) -> Optional[Dict]:
        """加载变体"""
        filepath = f"{self.population_dir}/{variant_id}.json"
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_variants(self) -> List[str]:
        """列出所有变体"""
        if not os.path.exists(self.population_dir):
            return []
        
        variants = []
        for f in os.listdir(self.population_dir):
            if f.endswith('.json'):
                variants.append(f.replace('.json', ''))
        return variants
    
    def generate_prompt(self, variant: Dict) -> str:
        """根据变体基因生成Prompt"""
        genome = variant['genome']
        
        # 基础角色
        role = genome['cognitive'].get('role', 'assistant')
        
        # Prompt模板
        base_prompt = genome['cognitive'].get('prompt', 'You are a helpful assistant.')
        
        # 社交风格
        style = genome['social'].get('style', 'direct')
        
        # 组合
        prompt = f"""你是一个{role}。

{base_prompt}

工作风格: {style}
学习率: {genome['adaptive'].get('learning_rate', 0.1)}
探索/利用比率: {genome['adaptive'].get('explore_ratio', 0.5)}

你偏好使用的工具: {', '.join(genome['cognitive'].get('tools', ['read', 'write']))}

请根据任务要求，自主决定最佳行动方案。
"""
        return prompt
    
    def create_agent_config(self, variant: Dict) -> Dict:
        """创建Agent配置"""
        return {
            'model': 'minimax/MiniMax-M2.1',
            'system_prompt': self.generate_prompt(variant),
            'variant_id': variant['variant_id'],
            'generation': variant.get('generation', 0),
            'parent_ids': variant.get('parent_ids', []),
            'fitness': variant['phenotype'].get('fitness', 0)
        }
    
    def export_population(self, population: List[Dict]):
        """导出整个种群"""
        for variant in population:
            self.save_variant(variant)
        print(f"[OpenClaw] 导出种群: {len(population)} 个变体")
    
    def import_population(self) -> List[Dict]:
        """导入种群"""
        population = []
        for variant_id in self.list_variants():
            variant = self.load_variant(variant_id)
            if variant:
                population.append(variant)
        print(f"[OpenClaw] 导入种群: {len(population)} 个变体")
        return population


class SwarmCommunicator:
    """群体通信器"""
    
    def __init__(self):
        self.messages = []
        self.subscriptions = {}
    
    def send(self, sender_id: str, receiver_id: str, content: str):
        """发送消息"""
        msg = {
            'id': len(self.messages),
            'sender': sender_id,
            'receiver': receiver_id,
            'content': content,
            'timestamp': None  # would use datetime
        }
        self.messages.append(msg)
        return msg
    
    def broadcast(self, sender_id: str, content: str):
        """广播消息"""
        msg = {
            'id': len(self.messages),
            'sender': sender_id,
            'receiver': None,  # broadcast
            'content': content,
            'timestamp': None
        }
        self.messages.append(msg)
        return msg
    
    def get_messages(self, agent_id: str = None) -> List[Dict]:
        """获取消息"""
        if agent_id is None:
            return self.messages
        
        # 返回发给该agent的消息
        return [
            m for m in self.messages 
            if m['receiver'] == agent_id or m['receiver'] is None
        ]


# 演示
def demo():
    """演示OpenClaw集成"""
    print("="*60)
    print("OpenClaw Integration Demo")
    print("="*60)
    
    # 创建测试变体
    variant = {
        'variant_id': 'test_001',
        'generation': 1,
        'parent_ids': ['seed_001'],
        'genome': {
            'cognitive': {
                'role': 'explorer',
                'prompt': '你是一个勇敢的探索者',
                'tools': ['browser', 'read']
            },
            'social': {
                'style': 'direct',
                'cooperation': 0.7
            },
            'adaptive': {
                'learning_rate': 0.1,
                'explore_ratio': 0.6
            }
        },
        'phenotype': {
            'fitness': 0.85,
            'tasks_completed': 10
        }
    }
    
    # 创建集成器
    integrator = OpenClawIntegrator()
    
    # 保存
    path = integrator.save_variant(variant)
    print(f"\n[Saved] {path}")
    
    # 生成Prompt
    prompt = integrator.generate_prompt(variant)
    print(f"\n[Generated Prompt]")
    print(prompt[:200] + "...")
    
    # 创建Agent配置
    config = integrator.create_agent_config(variant)
    print(f"\n[Agent Config]")
    print(f"  Model: {config['model']}")
    print(f"  Variant ID: {config['variant_id']}")
    print(f"  Generation: {config['generation']}")
    
    # 测试通信
    comm = SwarmCommunicator()
    comm.broadcast('agent_001', '发现有趣的内容!')
    comm.send('agent_002', 'agent_003', '需要帮助')
    
    print(f"\n[Messages]")
    for msg in comm.get_messages():
        receiver = msg['receiver'] or 'ALL'
        print(f"  {msg['sender']} -> {receiver}: {msg['content'][:30]}")


if __name__ == "__main__":
    demo()
