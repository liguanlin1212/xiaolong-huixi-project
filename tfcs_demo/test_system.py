#!/usr/bin/env python3
"""
系统测试脚本
用于验证系统核心功能是否正常工作
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("=== 系统测试开始 ===")

# 测试核心模块导入
try:
    from core.enums import NarrativeType
    print("✅ 成功导入 core.enums")
except Exception as e:
    print(f"❌ 导入 core.enums 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 AI 能力层
try:
    from ai.inference.npu_runner import classify_text
    print("✅ 成功导入 ai.inference.npu_runner")
    
    # 测试文本分类
    test_text = "刘鑫也是受害者，她当时也很害怕"
    result = classify_text(test_text)
    print(f"✅ 成功执行文本分类")
    print(f"   分类结果: {result}")
except Exception as e:
    print(f"❌ 导入或执行 ai.inference.npu_runner 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试业务层
try:
    from app.services.narrative_service import analyse_text_entry
    print("✅ 成功导入 app.services.narrative_service")
    
    # 测试文本分析
    test_entry = {
        "time": "2023-01-01",
        "text": "刘鑫也是受害者，她当时也很害怕"
    }
    result = analyse_text_entry(test_entry)
    print(f"✅ 成功执行文本分析")
    print(f"   分析结果: {result}")
except Exception as e:
    print(f"❌ 导入或执行 app.services.narrative_service 失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.services.judgement_service import build_timeline
    print("✅ 成功导入 app.services.judgement_service")
    
    # 测试时间轴生成
    test_entries = [
        {
            "time": "2023-01-02",
            "text": "聊天记录显示她提前意识到危险",
            "narrative": NarrativeType.EVIDENCE,
            "confidence": 0.9
        },
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕",
            "narrative": NarrativeType.EMOTIONAL,
            "confidence": 0.8
        }
    ]
    timeline = build_timeline(test_entries)
    print(f"✅ 成功执行时间轴生成")
    print(f"   时间轴长度: {len(timeline)}")
    print(f"   排序结果: {[entry['time'] for entry in timeline]}")
except Exception as e:
    print(f"❌ 导入或执行 app.services.judgement_service 失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 UI 层
try:
    from app.ui.timeline_view import display_timeline
    print("✅ 成功导入 app.ui.timeline_view")
    
    # 测试时间轴显示
    test_timeline = [
        {
            "time": "2023-01-01",
            "text": "测试文本",
            "narrative": NarrativeType.EMOTIONAL,
            "confidence": 0.8
        }
    ]
    print("\n=== 测试时间轴显示 ===")
    display_timeline(test_timeline)
except Exception as e:
    print(f"❌ 导入或执行 app.ui.timeline_view 失败: {e}")
    import traceback
    traceback.print_exc()

print("=== 系统测试完成 ===")
