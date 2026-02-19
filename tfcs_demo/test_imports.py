import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("sys.path:", sys.path)

# 测试导入
try:
    import core.enums
    print("Successfully imported core.enums")
except Exception as e:
    print("Error importing core.enums:", e)

try:
    from ai.inference.npu_runner import classify_text
    print("Successfully imported classify_text")
    # 测试分类函数
    test_result = classify_text("测试文本")
    print("Test classification result:", test_result)
except Exception as e:
    print("Error importing classify_text:", e)
    import traceback
    traceback.print_exc()
