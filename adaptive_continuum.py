# -*- coding: utf-8 -*-
"""
Adaptive Continuum - 真正的自适应持续思维系统
像生物一样适应环境的思维链
"""

import random
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ==================== 核心类 ====================

class ThoughtMode(Enum):
    """思维模式"""
    DRIFT = "drift"      # 漫游 - 探索
    FOCUS = "focus"      # 专注 - 执行
    HIBERNATE = "hibernate"  # 休眠 - 等待


@dataclass
class Agent:
    """智能体 - 有生命的思维"""
    id: str
    name: str
    
    # 基因 - 策略参数
    speed: float = 0.5      # 反应速度
    caution: float = 0.5    # 谨慎程度  
    energy: float = 0.5     # 能量效率
    curiosity: float = 0.5  # 好奇心
    
    # 状态
    energy_level: float = 1.0
    alive: bool = True
    age: int = 0
    thoughts: List[str] = field(default_factory=list)
    
    def mutate(self, rate: float = 0.2):
        """变异"""
        if random.random() < rate:
            trait = random.choice(['speed', 'caution', 'energy', 'curiosity'])
            delta = random.uniform(-0.15, 0.15)
            setattr(self, trait, max(0.1, min(1.0, getattr(self, trait) + delta)))
    
    def copy(self) -> 'Agent':
        """复制"""
        return Agent(
            id=f"agent_{random.randint(10000,99999)}",
            name=self.name,
            speed=self.speed,
            caution=self.caution,
            energy=self.energy,
            curiosity=self.curiosity,
            energy_level=self.energy_level,
            age=0
        )


@dataclass
class Environment:
    """环境"""
    name: str
    pressure: str  # speed, caution, energy, curiosity, chaos
    difficulty: float = 0.5
    
    def __str__(self):
        return f"{self.name} [{self.pressure}:{self.difficulty}]"


# ==================== 思维系统 ====================

class AdaptiveMind:
    """自适应思维系统"""
    
    def __init__(self, name: str):
        self.name = name
        self.agents: List[Agent] = []
        self.environment: Environment = Environment("Neutral", "balance", 0.3)
        self.generation = 0
        self.thought_log: List[str] = []
        
        # 初始化种群
        self._init_agents(15)
    
    def _init_agents(self, count: int):
        """初始化智能体 - 多样性"""
        types = [
            ('Explorer', 0.8, 0.3, 0.5, 0.9),   # 好奇、快速
            ('Thinker', 0.4, 0.8, 0.6, 0.7),    # 谨慎、思考
            ('Survivor', 0.3, 0.6, 0.9, 0.4),   # 节能、保守
            ('Social', 0.5, 0.5, 0.5, 0.5),     # 平衡
            ('Hunter', 0.9, 0.2, 0.7, 0.6),     # 激进
        ]
        
        for i in range(count):
            name, speed, caution, energy, curiosity = random.choice(types)
            agent = Agent(
                id=f"gen0_{i}",
                name=name,
                speed=speed,
                caution=caution,
                energy=energy,
                curiosity=curiosity
            )
            self.agents.append(agent)
        
        self.thought_log.append(f"[Init] Created {count} agents")
    
    def set_environment(self, env: Environment):
        """设置环境"""
        self.environment = env
        self.thought_log.append(f"[Env] Changed to {env}")
    
    def think(self) -> str:
        """每个智能体产生一个想法"""
        thoughts = []
        
        for agent in self.agents:
            if not agent.alive:
                continue
            
            # 根据策略产生想法
            thought = self._generate_thought(agent)
            agent.thoughts.append(thought)
            
            # 消耗能量
            energy_cost = 0.01 * (1.1 - agent.energy)
            agent.energy_level -= energy_cost
            
            # 能量太低则休眠
            if agent.energy_level < 0.2:
                agent.alive = False
            
            thoughts.append(f"{agent.name}: {thought}")
        
        return thoughts
    
    def _generate_thought(self, agent: Agent) -> str:
        """根据基因产生想法"""
        
        # 环境压力影响思维
        env = self.environment
        
        if env.pressure == "speed":
            if agent.speed > 0.6:
                return "快速反应！立即行动！"
            else:
                return "需要加快速度..."
        
        elif env.pressure == "caution":
            if agent.caution > 0.6:
                return "小心为上，先观察环境"
            else:
                return "风险不大，直接上"
        
        elif env.pressure == "energy":
            if agent.energy > 0.7:
                return "保存能量，缓慢行动"
            else:
                return "精力充沛，活跃行动"
        
        elif env.pressure == "curiosity":
            if agent.curiosity > 0.6:
                return "这很有趣，让我探索更多"
            else:
                return "保持现状"
        
        elif env.pressure == "chaos":
            return "混乱中寻找机会"
        
        else:
            return "继续思考..."
    
    def survive(self) -> List[Agent]:
        """环境选择 - 适者生存"""
        survivors = []
        
        for agent in self.agents:
            if not agent.alive:
                continue
            
            # 计算生存概率
            chance = self._calculate_survival(agent)
            
            if random.random() < chance:
                agent.age += 1
                agent.energy_level = min(1.0, agent.energy_level + 0.1)
                survivors.append(agent)
            else:
                agent.alive = False
        
        return survivors
    
    def _calculate_survival(self, agent: Agent) -> float:
        """计算生存概率"""
        env = self.environment
        s = agent
        d = env.difficulty
        
        # 不同环境需要不同策略
        if env.pressure == "speed":
            required = s.speed
            survival = required * (1 - d * 0.5) + 0.3
        
        elif env.pressure == "caution":
            required = s.caution
            survival = required * (1 - d * 0.5) + 0.3
        
        elif env.pressure == "energy":
            required = s.energy
            survival = required * (1 - d * 0.5) + 0.3
        
        elif env.pressure == "curiosity":
            required = s.curiosity
            survival = required * (1 - d * 0.5) + 0.3
        
        elif env.pressure == "chaos":
            survival = 0.3 + s.speed * 0.2 + s.caution * 0.2
            survival *= (1 - d * 0.5)
        
        else:
            survival = 0.6
        
        return max(0.2, min(0.95, survival))
    
    def reproduce(self, survivors: List[Agent]):
        """繁殖 - 遗传 + 变异"""
        if not survivors:
            self.thought_log.append("[Extinction] All agents died!")
            return
        
        new_agents = []
        
        # 精英保留
        survivors.sort(key=lambda a: (a.age, a.energy_level), reverse=True)
        
        for agent in survivors[:3]:
            new_agents.append(agent.copy())
        
        # 繁殖
        target = len(self.agents)
        while len(new_agents) < target:
            parent = random.choice(survivors)
            child = parent.copy()
            child.mutate(rate=0.3)
            child.id = f"gen{self.generation}_{len(new_agents)}"
            new_agents.append(child)
        
        self.agents = new_agents
        self.generation += 1
    
    def run_cycle(self) -> Dict:
        """运行一个周期"""
        # 1. 思考
        thoughts = self.think()
        
        # 2. 生存
        survivors = self.survive()
        
        # 3. 繁殖
        self.reproduce(survivors)
        
        # 4. 统计
        alive = sum(1 for a in self.agents if a.alive)
        
        return {
            'generation': self.generation,
            'alive': alive,
            'thoughts': thoughts[:3] if thoughts else []
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        alive = [a for a in self.agents if a.alive]
        
        if alive:
            avg_speed = sum(a.speed for a in alive) / len(alive)
            avg_caution = sum(a.caution for a in alive) / len(alive)
            avg_energy = sum(a.energy for a in alive) / len(alive)
            avg_curiosity = sum(a.curiosity for a in alive) / len(alive)
        else:
            avg_speed = avg_caution = avg_energy = avg_curiosity = 0
        
        # 统计类型
        types = {}
        for a in alive:
            types[a.name] = types.get(a.name, 0) + 1
        
        return {
            'alive': len(alive),
            'speed': avg_speed,
            'caution': avg_caution,
            'energy': avg_energy,
            'curiosity': avg_curiosity,
            'types': types
        }


# ==================== 主程序 ====================

def run_adaptive_system():
    """运行自适应系统"""
    
    print("\n" + "="*70)
    print("ADAPTIVE CONTINUUM - Self-Adapting Mind System")
    print("="*70)
    
    # 创建系统
    mind = AdaptiveMind("Alpha")
    
    # 环境变化
    environments = [
        Environment("Training Ground", "speed", 0.5),
        Environment("Research Lab", "curiosity", 0.6),
        Environment("Wilderness", "energy", 0.7),
        Environment("Battle Zone", "speed", 0.8),
        Environment("Meditation Chamber", "caution", 0.4),
        Environment("Chaos Realm", "chaos", 0.9),
    ]
    
    # 运行多代
    total_cycles = 30
    
    for cycle in range(total_cycles):
        # 周期性改变环境
        env = environments[cycle % len(environments)]
        mind.set_environment(env)
        
        # 运行周期
        result = mind.run_cycle()
        stats = mind.get_stats()
        
        # 打印状态
        types_str = ', '.join([f"{k}:{v}" for k,v in stats['types'].items()])
        
        print(f"[{cycle+1:2d}] Gen{result['generation']:2d} | "
              f"Alive:{stats['alive']:2d} | "
              f"Speed:{stats['speed']:.2f} "
              f"Caution:{stats['caution']:.2f} "
              f"Energy:{stats['energy']:.2f} "
              f"Curiosity:{stats['curiosity']:.2f} | "
              f"{types_str}")
    
    # 最终结果
    print("\n" + "="*70)
    print("FINAL ADAPTIVE STATE")
    print("="*70)
    
    final_stats = mind.get_stats()
    
    print(f"\nSurvivors: {final_stats['alive']}")
    print(f"\nAverage Traits:")
    print(f"  Speed: {final_stats['speed']:.3f}")
    print(f"  Caution: {final_stats['caution']:.3f}")
    print(f"  Energy: {final_stats['energy']:.3f}")
    print(f"  Curiosity: {final_stats['curiosity']:.3f}")
    
    print(f"\nSpecies Distribution:")
    for name, count in final_stats['types'].items():
        print(f"  {name}: {count}")
    
    # 打印一些想法
    print(f"\nSample Thoughts:")
    alive_agents = [a for a in mind.agents if a.alive][:5]
    for agent in alive_agents:
        if agent.thoughts:
            print(f"  {agent.name}: {agent.thoughts[-1]}")


if __name__ == "__main__":
    run_adaptive_system()
