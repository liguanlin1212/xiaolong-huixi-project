import os
import sys
import pytest

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    设置测试环境
    """
    print("设置测试环境...")
    # 可以在这里添加测试环境的设置代码
    yield
    print("清理测试环境...")

@pytest.fixture
def test_data():
    """
    提供测试数据
    """
    return [
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕"
        },
        {
            "time": "2023-01-02",
            "text": "聊天记录显示她提前意识到危险"
        },
        {
            "time": "2023-01-03",
            "text": "法院判决认定不构成刑事责任"
        }
    ]

# 配置测试超时
@pytest.fixture(scope="function", autouse=True)
def timeout():
    """
    测试超时设置
    """
    import time
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(f"警告: 测试执行时间过长: {elapsed_time:.2f} 秒")
