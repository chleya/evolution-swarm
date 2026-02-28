# -*- coding: utf-8 -*-
"""
Memory Tree - 记忆树系统
基于 Memory-Like-A-Tree 理念
让知识像树一样生长
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import uuid


# ==================== 数据结构 ====================

@dataclass
class MemoryNode:
    """记忆节点"""
    id: str
    content: str
    parent_id: Optional[str] = None
    children_ids: List[str] = None
    confidence: float = 1.0  # 置信度 0-1
    access_count: int = 0
    created_at: str = None
    last_accessed: str = None
    decay_factor: float = 0.95  # 衰减因子
    metadata: Dict = None
    status: str = "active"  # active / archived  # 新增：状态标记
    
    def __post_init__(self):
        if self.children_ids is None:
            self.children_ids = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.last_accessed is None:
            self.last_accessed = self.created_at
        if self.metadata is None:
            self.metadata = {}
    
    def calculate_confidence(self) -> float:
        """计算当前置信度 - 基于访问和时间衰减"""
        # 时间衰减
        age_hours = (time.time() - datetime.fromisoformat(self.last_accessed).timestamp()) / 3600
        time_decay = max(0.1, 1.0 - age_hours * 0.01)  # 每小时衰减1%
        
        # 访问次数增益
        access_boost = min(0.2, self.access_count * 0.02)  # 最多+20%
        
        # 置信度 = 基础 * 时间衰减 + 访问增益
        confidence = (self.confidence * time_decay) + access_boost
        return min(1.0, max(0.0, confidence))


@dataclass
class MemoryTreeConfig:
    """记忆树配置"""
    max_nodes: int = 10000  # 最大节点数
    decay_interval_hours: int = 24  # 衰减检查间隔
    min_confidence: float = 0.1  # 最小置信度阈值
    prune_threshold: float = 0.05  # 剪枝阈值
    auto_decay_enabled: bool = True
    confidence_boost_on_access: bool = True


# ==================== 核心类 ====================

class MemoryTree:
    """记忆树 - 让知识像树一样生长"""
    
    def __init__(self, root_content: str = "Root", config: MemoryTreeConfig = None):
        self.config = config or MemoryTreeConfig()
        self.nodes: Dict[str, MemoryNode] = {}
        
        # 创建根节点
        self.root_id = self.create_node(root_content, parent_id=None)
    
    def create_node(self, content: str, parent_id: str = None, metadata: Dict = None) -> str:
        """创建新记忆节点"""
        node_id = str(uuid.uuid4())[:8]
        
        # 如果没有指定父节点，默认连接到根节点（如果根节点已存在）
        if parent_id is None and hasattr(self, 'root_id'):
            parent_id = self.root_id
        
        node = MemoryNode(
            id=node_id,
            content=content,
            parent_id=parent_id,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        
        # 更新父节点的children
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children_ids.append(node_id)
        
        # 检查是否需要剪枝
        if len(self.nodes) > self.config.max_nodes:
            self._prune_low_confidence()
        
        return node_id
    
    def access_node(self, node_id: str) -> Optional[MemoryNode]:
        """访问节点 - 提升置信度"""
        if node_id not in self.nodes:
            return None
        
        node = self.nodes[node_id]
        node.access_count += 1
        node.last_accessed = datetime.now().isoformat()
        
        # 访问时提升置信度
        if self.config.confidence_boost_on_access:
            node.confidence = min(1.0, node.confidence + 0.05)
        
        return node
    
    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def search_by_content(self, keyword: str, include_archived: bool = True) -> List[MemoryNode]:
        """按内容搜索
        
        Args:
            keyword: 搜索关键词
            include_archived: 是否包含归档记忆
        """
        results = []
        for node in self.nodes.values():
            if keyword.lower() in node.content.lower():
                # 根据状态过滤
                if node.status == "active" or include_archived:
                    results.append(node)
        return results
    
    def get_archived_memories(self) -> List[MemoryNode]:
        """获取归档记忆"""
        return [n for n in self.nodes.values() if n.status == "archived"]
    
    def reactivate_memory(self, node_id: str) -> bool:
        """重新激活归档记忆
        
        重新访问时自动激活
        """
        if node_id in self.nodes:
            if self.nodes[node_id].status == "archived":
                self.nodes[node_id].status = "active"
                # 提升置信度
                self.nodes[node_id].confidence = min(1.0, self.nodes[node_id].confidence + 0.3)
                print(f"[Memory Tree] Reactivated memory: {node_id[:8]}")
            # 无论什么状态，访问都会提升置信度
            self.nodes[node_id].access_count += 1
            self.nodes[node_id].last_accessed = datetime.now().isoformat()
            return True
        return False
    
    def get_path_to_root(self, node_id: str) -> List[MemoryNode]:
        """获取到根节点的路径"""
        path = []
        current_id = node_id
        
        while current_id and current_id in self.nodes:
            path.append(self.nodes[current_id])
            current_id = self.nodes[current_id].parent_id
        
        return path
    
    def get_children(self, node_id: str) -> List[MemoryNode]:
        """获取子节点"""
        if node_id not in self.nodes:
            return []
        
        children = []
        for child_id in self.nodes[node_id].children_ids:
            if child_id in self.nodes:
                children.append(self.nodes[child_id])
        return children
    
    def update_confidence(self, node_id: str, new_confidence: float):
        """更新节点置信度"""
        if node_id in self.nodes:
            self.nodes[node_id].confidence = max(0, min(1.0, new_confidence))
    
    def _prune_low_confidence(self):
        """标记低置信度节点为归档，不删除"""
        archived_count = 0
        
        for node_id, node in self.nodes.items():
            if node_id == self.root_id:
                continue  # 不处理根节点
            
            # 计算当前置信度
            current_conf = node.calculate_confidence()
            
            # 如果低于阈值，标记为归档
            if current_conf < self.config.prune_threshold:
                node.status = "archived"
                archived_count += 1
        
        if archived_count > 0:
            print(f"[Memory Tree] Archived {archived_count} low-confidence nodes (not deleted)")
        
        # 不再真正删除任何节点！
        # 所有记忆都会被保留，只是标记为 archived 状态
    
    def _delete_node(self, node_id: str):
        """删除节点"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # 从父节点移除
        if node.parent_id and node.parent_id in self.nodes:
            if node_id in self.nodes[node.parent_id].children_ids:
                self.nodes[node.parent_id].children_ids.remove(node_id)
        
        # 递归删除子节点
        for child_id in node.children_ids[:]:
            self._delete_node(child_id)
        
        del self.nodes[node_id]
    
    def get_tree_stats(self) -> Dict:
        """获取树统计"""
        confidences = [n.calculate_confidence() for n in self.nodes.values()]
        
        active_count = sum(1 for n in self.nodes.values() if n.status == "active")
        archived_count = sum(1 for n in self.nodes.values() if n.status == "archived")
        
        return {
            'total_nodes': len(self.nodes),
            'active_nodes': active_count,
            'archived_nodes': archived_count,
            'avg_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'avg_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'max_confidence': max(confidences) if confidences else 0,
            'min_confidence': min(confidences) if confidences else 0,
            'root_id': self.root_id,
        }
    
    def export_to_dict(self) -> Dict:
        """导出为字典"""
        return {
            'config': asdict(self.config),
            'root_id': self.root_id,
            'nodes': {k: asdict(v) for k, v in self.nodes.items()}
        }
    
    def import_from_dict(self, data: Dict):
        """从字典导入"""
        self.config = MemoryTreeConfig(**data.get('config', {}))
        self.root_id = data.get('root_id', '')
        self.nodes = {k: MemoryNode(**v) for k, v in data.get('nodes', {}).items()}
    
    def save_to_file(self, filepath: str):
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.export_to_dict(), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.import_from_dict(data)


# ==================== 知识流动 ====================

class KnowledgeFlow:
    """知识流动 - 跨记忆树的知识传递"""
    
    def __init__(self):
        self.trees: Dict[str, MemoryTree] = {}  # 多个记忆树
    
    def create_tree(self, tree_id: str, root_content: str) -> MemoryTree:
        """创建新记忆树"""
        tree = MemoryTree(root_content)
        self.trees[tree_id] = tree
        return tree
    
    def get_tree(self, tree_id: str) -> Optional[MemoryTree]:
        """获取记忆树"""
        return self.trees.get(tree_id)
    
    def cross_tree_search(self, keyword: str) -> Dict[str, List[MemoryNode]]:
        """跨树搜索"""
        results = {}
        for tree_id, tree in self.trees.items():
            results[tree_id] = tree.search_by_content(keyword)
        return results
    
    def merge_trees(self, source_tree_id: str, target_tree_id: str, node_id: str):
        """跨树迁移知识"""
        source_tree = self.trees.get(source_tree_id)
        target_tree = self.trees.get(target_tree_id)
        
        if not source_tree or not target_tree:
            return None
        
        source_node = source_tree.get_node(node_id)
        if not source_node:
            return None
        
        # 在目标树中创建新节点
        new_node_id = target_tree.create_node(
            content=source_node.content,
            metadata={'merged_from': f"{source_tree_id}:{node_id}"}
        )
        
        return new_node_id


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Memory Tree Test")
    print("=" * 60)
    
    # 创建记忆树
    tree = MemoryTree("Evolution Knowledge")
    
    # 创建记忆节点
    id1 = tree.create_node("核心概念: 演化", metadata={'topic': 'evolution'})
    id2 = tree.create_node("机制: 选择压力", parent_id=id1, metadata={'topic': 'mechanism'})
    id3 = tree.create_node("机制: 变异", parent_id=id1, metadata={'topic': 'mechanism'})
    id4 = tree.create_node("应用: 神经网络", parent_id=id2, metadata={'topic': 'application'})
    
    print(f"\nCreated nodes:")
    print(f"  Root -> {id1} (演化)")
    print(f"    -> {id2} (选择压力)")
    print(f"    -> {id3} (变异)")
    print(f"      -> {id4} (神经网络)")
    
    # 访问节点
    tree.access_node(id2)
    tree.access_node(id4)
    
    # 搜索
    results = tree.search_by_content("演化")
    print(f"\nSearch '演化': {len(results)} results")
    
    # 统计
    stats = tree.get_tree_stats()
    print(f"\nTree Stats:")
    print(f"  Total nodes: {stats['total_nodes']}")
    print(f"  Avg confidence: {stats['avg_confidence']:.3f}")
    
    # 路径
    path = tree.get_path_to_root(id4)
    print(f"\nPath to root (神经网络):")
    for node in path:
        print(f"  - {node.content[:20]}")
    
    print("\n[SUCCESS] Memory Tree is working!")
