# -*- coding: utf-8 -*-
"""
Continuum Engine - 持续思维链引擎
实现: 心跳循环 + 状态机 + 思维缓冲 + 仲裁者
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


# ==================== 数据结构 ====================

class ThoughtType(Enum):
    """思维类型"""
    DRIFT = "drift"      # 漫游态
    FOCUS = "focus"      # 专注态
    INTEGRATE = "integrate"  # 整合态
    EXECUTE = "execute"  # 执行态


@dataclass
class ThoughtNode:
    """思维节点"""
    id: str
    content: str
    type: ThoughtType
    intensity: float = 0.5  # 0.1-1.0
    tags: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    associated_memory_ids: List[str] = field(default_factory=list)


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TaskObject:
    """任务对象"""
    id: str
    description: str
    priority: int = 5  # 1-10
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[str] = None


# ==================== 核心组件 ====================

class StreamBuffer:
    """思维缓冲流 - 短期记忆"""
    
    def __init__(self, max_size: int = 20):
        self.max_size = max_size
        self.buffer: List[ThoughtNode] = []
    
    def add(self, thought: ThoughtNode):
        self.buffer.append(thought)
        if len(self.buffer) > self.max_size:
            return self.buffer.pop(0)
        return None
    
    def get_context(self) -> str:
        """获取上下文"""
        if not self.buffer:
            return ""
        recent = self.buffer[-5:]
        return "\n".join([f"[{t.type.value}] {t.content[:50]}" for t in recent])
    
    def get_recent_topics(self) -> List[str]:
        """获取最近主题"""
        topics = []
        for t in self.buffer[-5:]:
            topics.extend(t.tags)
        return list(set(topics))
    
    def get_state(self) -> Dict:
        """获取内部状态"""
        if not self.buffer:
            return {'avg_intensity': 0, 'count': 0}
        
        intensities = [t.intensity for t in self.buffer]
        return {
            'avg_intensity': sum(intensities) / len(intensities),
            'count': len(self.buffer),
            'last_type': self.buffer[-1].type.value
        }
    
    def is_full(self) -> bool:
        return len(self.buffer) >= self.max_size


class Subconscious:
    """潜意识层 - 长期记忆"""
    
    def __init__(self):
        self.memories: List[MemoryEntry] = []
    
    def store(self, entry: MemoryEntry):
        self.memories.append(entry)
        # 限制大小
        if len(self.memories) > 1000:
            self.memories = self.memories[-500:]
    
    def retrieve(self, topics: List[str], limit: int = 3) -> List[MemoryEntry]:
        """基于主题检索"""
        if not topics or not self.memories:
            # 返回最近的记忆
            return self.memories[-limit:] if self.memories else []
        
        # 简单匹配
        results = []
        for mem in reversed(self.memories):
            if any(tag in topics for tag in mem.tags):
                results.append(mem)
            if len(results) >= limit:
                break
        
        # 如果没有匹配的，返回随机的
        if not results:
            results = random.sample(self.memories, min(limit, len(self.memories)))
        
        return results
    
    def compress_and_store(self, thought: ThoughtNode):
        """压缩并存储"""
        entry = MemoryEntry(
            id=f"mem_{thought.id}",
            content=thought.content[:200],  # 压缩
            importance=thought.intensity,
            tags=thought.tags
        )
        self.store(entry)


class Arbitrator:
    """仲裁者 - 决定状态"""
    
    def __init__(self):
        self.drift_timer = 0
        self.last_task_time = time.time()
    
    def decide(self, 
               external_tasks: List[TaskObject],
               internal_state: Dict,
               relevant_memories: List[MemoryEntry]) -> ThoughtType:
        """决定当前状态"""
        
        # 有外部任务 → 专注态
        if external_tasks and external_tasks[0].priority >= 8:
            self.last_task_time = time.time()
            return ThoughtType.FOCUS
        
        # 任务队列不为空 → 专注态
        if external_tasks:
            self.last_task_time = time.time()
            return ThoughtType.FOCUS
        
        # 长时间无任务 → 漫游态
        idle_time = time.time() - self.last_task_time
        if idle_time > 10:  # 10秒无任务
            self.drift_timer += 1
        else:
            self.drift_timer = max(0, self.drift_timer - 1)
        
        # 整合态 - 刚完成任务后
        if internal_state.get('last_type') == 'execute':
            return ThoughtType.INTEGRATE
        
        # 漫游态
        return ThoughtType.DRIFT
    
    def get_system_prompt(self, state: ThoughtType) -> str:
        """获取状态提示"""
        prompts = {
            ThoughtType.DRIFT: "保持开放性，允许联想自由飞翔，接受意外的思维跳转",
            ThoughtType.FOCUS: "保持逻辑严密，专注于当前问题，避免分心",
            ThoughtType.INTEGRATE: "回顾刚才的思考，将其与更宏观的主题联系起来",
            ThoughtType.EXECUTE: "执行具体行动，注意细节"
        }
        return prompts.get(state, "保持自然思考")


class Generator:
    """生成器 - 产生思维"""
    
    # 思维模板
    DRIFT_TEMPLATES = [
        "这让我想到...",
        "也许可以换个角度...",
        "有没有可能...",
        "让我联想到了...",
        "或许..."
    ]
    
    FOCUS_TEMPLATES = [
        "分析这个问题...",
        "首先...",
        "其次...",
        "因此...",
        "结论是..."
    ]
    
    INTEGRATE_TEMPLATES = [
        "回顾一下...",
        "总结刚才...",
        "接下来...",
        "还可以...",
        "还有什么..."
    ]
    
    def generate(self, state: ThoughtType, context: str, topics: List[str]) -> ThoughtNode:
        """生成思维"""
        
        # 选择模板
        if state == ThoughtType.DRIFT:
            template = random.choice(self.DRIFT_TEMPLATES)
            content = f"{template} {random.choice(topics) if topics else '思考中...'}"
            intensity = random.uniform(0.3, 0.6)
        elif state == ThoughtType.FOCUS:
            template = random.choice(self.FOCUS_TEMPLATES)
            content = f"{template} {context[:30]}"
            intensity = random.uniform(0.7, 1.0)
        elif state == ThoughtType.INTEGRATE:
            template = random.choice(self.INTEGRATE_TEMPLATES)
            content = f"{template} {random.choice(topics) if topics else '整合中...'}"
            intensity = random.uniform(0.5, 0.8)
        else:
            content = "执行中..."
            intensity = 0.8
        
        return ThoughtNode(
            id=f"thought_{int(time.time()*1000)}",
            content=content,
            type=state,
            intensity=intensity,
            tags=topics[-2:] if topics else []
        )


class ContinuumEngine:
    """持续思维链引擎 - 核心"""
    
    def __init__(self, name: str = "Continuum"):
        self.name = name
        self.stream_buffer = StreamBuffer(max_size=20)
        self.subconscious = Subconscious()
        self.arbitrator = Arbitrator()
        self.generator = Generator()
        self.task_queue: List[TaskObject] = []
        self.is_running = False
        self.thought_count = 0
    
    def add_task(self, task: TaskObject):
        """添加外部任务"""
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: -t.priority)
    
    async def heartbeat_loop(self, max_iterations: int = 50):
        """心跳循环 - 永不停止"""
        self.is_running = True
        
        print(f"\n{'='*60}")
        print(f"{self.name} 启动 - 持续思维链引擎")
        print(f"{'='*60}\n")
        
        for i in range(max_iterations):
            # 1. 仲裁者决定状态
            relevant_memories = self.subconscious.retrieve(
                self.stream_buffer.get_recent_topics()
            )
            
            state = self.arbitrator.decide(
                external_tasks=self.task_queue,
                internal_state=self.stream_buffer.get_state(),
                relevant_memories=relevant_memories
            )
            
            # 2. 生成思维
            thought = self.generator.generate(
                state=state,
                context=self.stream_buffer.get_context(),
                topics=self.stream_buffer.get_recent_topics()
            )
            
            # 3. 如果是执行态，处理任务
            if state == ThoughtType.FOCUS and self.task_queue:
                task = self.task_queue.pop(0)
                thought.content = f"[任务: {task.description}] {thought.content}"
                task.status = "completed"
            
            # 4. 加入缓冲流
            self.stream_buffer.add(thought)
            self.thought_count += 1
            
            # 5. 周期性压缩记忆
            if self.stream_buffer.is_full():
                oldest = self.stream_buffer.buffer[0]
                self.subconscious.compress_and_store(oldest)
            
            # 打印状态
            state_icon = {
                ThoughtType.DRIFT: "🌊",
                ThoughtType.FOCUS: "🎯",
                ThoughtType.INTEGRATE: "🔄",
                ThoughtType.EXECUTE: "⚡"
            }
            
            print(f"[{i+1}] {state_icon.get(state, '?')} {state.value:10} | "
                  f"{thought.content[:50]}... (intensity: {thought.intensity:.2f})")
            
            # 模拟心跳间隔
            await self.heartbeat_interval()
        
        print(f"\n{'='*60}")
        print(f"思维循环结束，共产生 {self.thought_count} 个思维")
        print(f"{'='*60}")
    
    async def heartbeat_interval(self):
        """心跳间隔"""
        # 模拟异步
        time.sleep(0.3)
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'thought_count': self.thought_count,
            'buffer_size': len(self.stream_buffer.buffer),
            'memory_count': len(self.subconscious.memories),
            'pending_tasks': len(self.task_queue)
        }


# ==================== 演示 ====================

def demo():
    """演示"""
    print("Continuum Engine Demo")
    print("="*60)
    
    engine = ContinuumEngine("Alpha")
    
    # 添加一些任务
    engine.add_task(TaskObject("task_1", "分析数据", priority=8))
    engine.add_task(TaskObject("task_2", "写报告", priority=5))
    
    # 运行（模拟）
    print("\n开始思维循环...\n")
    
    for i in range(20):
        # 仲裁
        relevant_memories = engine.subconscious.retrieve(
            engine.stream_buffer.get_recent_topics()
        )
        
        state = engine.arbitrator.decide(
            external_tasks=engine.task_queue,
            internal_state=engine.stream_buffer.get_state(),
            relevant_memories=relevant_memories
        )
        
        # 生成
        thought = engine.generator.generate(
            state=state,
            context=engine.stream_buffer.get_context(),
            topics=engine.stream_buffer.get_recent_topics()
        )
        
        # 执行任务
        if state == ThoughtType.FOCUS and engine.task_queue:
            task = engine.task_queue.pop(0)
            thought.content = f"[执行: {task.description}] {thought.content}"
        
        # 加入缓冲
        engine.stream_buffer.add(thought)
        engine.thought_count += 1
        
        # 压缩记忆
        if engine.stream_buffer.is_full():
            oldest = engine.stream_buffer.buffer[0]
            engine.subconscious.compress_and_store(oldest)
        
        # 打印
        icons = {
            ThoughtType.DRIFT: "[DRIFT]",
            ThoughtType.FOCUS: "[FOCUS]",
            ThoughtType.INTEGRATE: "[INTEGRATE]"
        }
        
        print(f"[{i+1:2d}] {icons.get(state, '[?]')} {state.value:10} | "
              f"{thought.content[:45]}")
    
    print(f"\n状态: {engine.get_status()}")


if __name__ == "__main__":
    demo()
