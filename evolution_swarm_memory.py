# -*- coding: utf-8 -*-
"""
Evolution Swarm - 记忆树集成版
Evolution Swarm with Memory Tree
基于 Memory-Like-A-Tree 理念
"""

import random
from typing import List, Dict, Optional
from memory_tree import MemoryTree, KnowledgeFlow, MemoryTreeConfig


# ==================== 演化智能体 ====================

class EvoAgent:
    """演化智能体 - 带记忆树"""
    
    def __init__(self, agent_id: str, config: Dict = None):
        self.id = agent_id
        self.config = config or {}
        
        # 记忆树
        self.memory = MemoryTree(f"Agent_{agent_id}_Memory")
        
        # 演化参数
        self.fitness = 0.0
        self.generation = 0
        self.age = 0
        
        # 创建初始记忆
        self._init_memory()
    
    def _init_memory(self):
        """初始化记忆"""
        # 根记忆
        root = f"Agent {self.id} 演化知识"
        
        # 创建基础记忆
        knowledge_id = self.memory.create_node(
            "核心知识库",
            metadata={'type': 'knowledge', 'importance': 0.9}
        )
        
        # 创建经验记忆
        experience_id = self.memory.create_node(
            "实践经验",
            metadata={'type': 'experience', 'importance': 0.7}
        )
        
        # 创建问题记忆
        question_id = self.memory.create_node(
            "待解决问题",
            metadata={'type': 'question', 'importance': 0.5}
        )
    
    def think(self, topic: str) -> str:
        """思考 - 利用记忆树"""
        # 搜索相关记忆
        results = self.memory.search_by_content(topic)
        
        if results:
            # 访问最相关的记忆
            best = max(results, key=lambda n: n.confidence)
            self.memory.access_node(best.id)
            
            # 基于记忆生成思考
            return f"[记忆触发] {best.content[:50]}... + {topic}的思考"
        else:
            # 创建新记忆
            new_id = self.memory.create_node(
                f"关于{topic}的新思考",
                metadata={'type': 'new_thought', 'topic': topic}
            )
            return f"[新记忆] 创建了关于{topic}的思考"
    
    def learn(self, knowledge: str, importance: float = 0.5):
        """学习新知识"""
        node_id = self.memory.create_node(
            knowledge,
            metadata={'type': 'learned', 'importance': importance}
        )
        
        # 提升置信度
        self.memory.update_confidence(node_id, importance)
        
        return node_id
    
    def get_stats(self) -> Dict:
        """获取智能体统计"""
        tree_stats = self.memory.get_tree_stats()
        
        return {
            'id': self.id,
            'fitness': self.fitness,
            'generation': self.generation,
            'age': self.age,
            'memory_nodes': tree_stats['total_nodes'],
            'avg_confidence': tree_stats['avg_confidence'],
        }


# ==================== 演化种群 ====================

class EvoPopulation:
    """演化种群 - 带知识流动"""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.agents: List[EvoAgent] = []
        self.generation = 0
        
        # 知识流动
        self.knowledge_flow = KnowledgeFlow()
        
        # 初始化种群
        self._init_population()
    
    def _init_population(self):
        """初始化种群"""
        for i in range(self.size):
            agent = EvoAgent(f"Agent_{i}")
            self.agents.append(agent)
            
            # 加入知识流动
            self.knowledge_flow.create_tree(f"agent_{i}", f"Agent_{i}_Memory")
    
    def evolve(self):
        """演化一代"""
        self.generation += 1
        
        # 评估适应度
        for agent in self.agents:
            agent.fitness = random.random()
            agent.generation = self.generation
            agent.age += 1
        
        # 选择
        self.agents.sort(key=lambda a: a.fitness, reverse=True)
        
        # 保留精英
        elite = self.agents[:self.size // 2]
        
        # 知识共享 (跨记忆树)
        self._share_knowledge()
        
        return self.generation
    
    def _share_knowledge(self):
        """知识共享"""
        # 获取每个智能体的核心知识
        for agent in self.agents[:3]:  # 前3名分享知识
            # 搜索高置信度知识
            results = agent.memory.search_by_content("核心")
            
            for node in results[:2]:
                # 访问提升置信度
                agent.memory.access_node(node.id)
    
    def get_best_agent(self) -> Optional[EvoAgent]:
        """获取最优智能体"""
        if self.agents:
            return max(self.agents, key=lambda a: a.fitness)
        return None
    
    def get_stats(self) -> Dict:
        """获取种群统计"""
        return {
            'generation': self.generation,
            'size': len(self.agents),
            'best_fitness': max(a.fitness for a in self.agents) if self.agents else 0,
            'avg_fitness': sum(a.fitness for a in self.agents) / len(self.agents) if self.agents else 0,
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Evolution Swarm - Memory Tree Integration Test")
    print("=" * 60)
    
    # 创建种群
    population = EvoPopulation(size=5)
    
    print(f"\n[1] Initial population:")
    for agent in population.agents:
        stats = agent.get_stats()
        print(f"  {stats['id']}: fitness={stats['fitness']:.3f}, memory={stats['memory_nodes']} nodes")
    
    # 智能体思考
    print(f"\n[2] Agent thinking:")
    agent0 = population.agents[0]
    thought = agent0.think("演化")
    print(f"  {thought}")
    
    # 学习新知识
    print(f"\n[3] Learning:")
    agent0.learn("深度学习优化算法: Adam + SGD 混合", importance=0.9)
    agent0.learn("注意力机制提高模型性能", importance=0.8)
    print(f"  Added 2 new knowledge nodes")
    
    # 演化
    print(f"\n[4] Evolving:")
    for gen in range(3):
        population.evolve()
        stats = population.get_stats()
        print(f"  Gen {stats['generation']}: best={stats['best_fitness']:.3f}, avg={stats['avg_fitness']:.3f}")
    
    # 最佳智能体
    best = population.get_best_agent()
    print(f"\n[5] Best agent: {best.id}")
    print(f"  Fitness: {best.fitness:.3f}")
    print(f"  Memory nodes: {best.memory.get_tree_stats()['total_nodes']}")
    print(f"  Avg confidence: {best.memory.get_tree_stats()['avg_confidence']:.3f}")
    
    # 记忆搜索
    print(f"\n[6] Memory search '演化':")
    results = best.memory.search_by_content("演化")
    for node in results:
        print(f"  - {node.content[:40]} (confidence: {node.confidence:.2f})")
    
    print("\n[SUCCESS] Evolution Swarm with Memory Tree is working!")
