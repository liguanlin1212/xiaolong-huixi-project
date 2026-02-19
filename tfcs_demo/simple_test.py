print("开始测试...")

try:
    import sys
    print(f"Python版本: {sys.version}")
    
    # 测试基本导入
    from ai.inference.npu_runner import classify_text
    print("成功导入classify_text")
    
    # 测试分类功能
    result = classify_text("测试文本")
    print(f"分类结果: {result}")
    
    print("测试成功!")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
