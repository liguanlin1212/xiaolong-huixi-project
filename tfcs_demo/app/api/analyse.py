import json
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from app.services.narrative_service import analyse_text_entry
    from app.services.judgement_service import build_timeline
    from app.ui.timeline_view import display_timeline
    
    def main():
        # 读取原始文本数据
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw_texts.json"))
        with open(data_path, "r", encoding="utf-8") as f:
            raw_entries = json.load(f)
        
        # 分析每个文本条目
        analysed_entries = []
        for entry in raw_entries:
            analysed_entry = analyse_text_entry(entry)
            analysed_entries.append(analysed_entry)
        
        # 构建时间轴
        timeline = build_timeline(analysed_entries)
        
        # 显示时间轴
        display_timeline(timeline)

    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
