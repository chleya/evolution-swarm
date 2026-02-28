# -*- coding: utf-8 -*-
"""
Evolutionary Swarm - Unit Tests
演化智能群 - 单元测试
"""

import unittest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evolution_swarm import EvolutionarySwarm


class TestEvolutionarySwarm(unittest.TestCase):
    """测试演化智能群"""
    
    def setUp(self):
        """测试前准备"""
        self.swarm = EvolutionarySwarm(
            population_size=10,
            mutation_rate=0.3
        )
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(len(self.swarm.population), 10)
        self.assertEqual(self.swarm.generation, 0)
        self.assertIsNotNone(self.swarm.modes)
        print("[OK] test_init")
    
    def test_add_task(self):
        """测试添加任务"""
        self.swarm.add_task("test_task", "测试任务")
        self.assertEqual(len(self.swarm.tasks), 1)
        self.assertEqual(self.swarm.tasks[0]['id'], "test_task")
        print("[OK] test_add_task")
    
    def test_run_once(self):
        """测试运行一代"""
        self.swarm.add_task("task1", "任务1")
        self.swarm.add_task("task2", "任务2")
        
        result = self.swarm.run_once()
        
        self.assertGreater(self.swarm.generation, 0)
        self.assertIn('avg_fitness', result)
        self.assertIn('best_fitness', result)
        print(f"[OK] test_run_once: {result}")
    
    def test_mutation(self):
        """测试变异"""
        parent = {
            'id': 'parent',
            'generation': 0,
            'mode': 'analytical',
            'depth': 5,
            'fitness': 0.8,
            'tasks_completed': 10,
            'successes': 8
        }
        
        child = self.swarm._mutate(parent)
        
        # 检查子代
        self.assertNotEqual(child['id'], parent['id'])
        self.assertEqual(child['generation'], 1)
        self.assertEqual(child['tasks_completed'], 0)
        print("[OK] test_mutation")
    
    def test_crossover(self):
        """测试交叉"""
        p1 = {'mode': 'analytical', 'depth': 5, 'generation': 2}
        p2 = {'mode': 'creative', 'depth': 7, 'generation': 3}
        
        child = self.swarm._crossover(p1, p2)
        
        # 检查子代
        self.assertIn(child['mode'], ['analytical', 'creative'])
        self.assertEqual(child['generation'], 4)
        print("[OK] test_crossover")
    
    def test_evolution(self):
        """测试演化多代"""
        self.swarm.add_task("task1", "任务1")
        
        initial_fitness = self.swarm.get_status()['avg_fitness']
        
        for _ in range(5):
            self.swarm.run_once()
        
        final_fitness = self.swarm.get_status()['avg_fitness']
        
        print(f"[OK] test_evolution: {initial_fitness:.2f} -> {final_fitness:.2f}")
    
    def test_status(self):
        """测试状态获取"""
        status = self.swarm.get_status()
        
        self.assertIn('generation', status)
        self.assertIn('population_size', status)
        self.assertIn('avg_fitness', status)
        self.assertIn('best_fitness', status)
        print(f"[OK] test_status: {status}")


class TestChainOfThought(unittest.TestCase):
    """测试思维链"""
    
    def test_modes_exist(self):
        """测试思维模式存在"""
        swarm = EvolutionarySwarm(population_size=5)
        
        expected_modes = ['analytical', 'creative', 'critical', 'systematic', 'intuitive']
        
        for mode in expected_modes:
            self.assertIn(mode, swarm.modes)
        
        print("[OK] test_modes_exist")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Running Evolutionary Swarm Tests")
    print("="*60 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestEvolutionarySwarm))
    suite.addTests(loader.loadTestsFromTestCase(TestChainOfThought))
    
    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 总结
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("All tests PASSED!")
    else:
        print(f"Tests failed: {len(result.failures)}, errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
