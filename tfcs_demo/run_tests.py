#!/usr/bin/env python3
"""
测试运行脚本

用于统一运行测试，包括单元测试和性能测试
"""

import os
import sys
import subprocess
import argparse

def run_unit_tests():
    """
    运行单元测试
    """
    print("\n=== 运行单元测试 ===")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    return result.returncode

def run_performance_tests():
    """
    运行性能测试
    """
    print("\n=== 运行性能测试 ===")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/performance/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    return result.returncode

def run_all_tests():
    """
    运行所有测试
    """
    print("\n=== 运行所有测试 ===")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    return result.returncode

def run_coverage():
    """
    运行测试覆盖率分析
    """
    print("\n=== 运行测试覆盖率分析 ===")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--cov=.", "--cov-report=term", "--cov-report=html"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    return result.returncode

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="测试运行脚本")
    parser.add_argument(
        "-t", "--test-type",
        choices=["all", "unit", "performance", "coverage"],
        default="all",
        help="测试类型"
    )
    
    args = parser.parse_args()
    
    if args.test_type == "unit":
        returncode = run_unit_tests()
    elif args.test_type == "performance":
        returncode = run_performance_tests()
    elif args.test_type == "coverage":
        returncode = run_coverage()
    else:  # all
        returncode = run_all_tests()
    
    if returncode == 0:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 测试失败，返回代码: {returncode}")
    
    return returncode

if __name__ == "__main__":
    sys.exit(main())
