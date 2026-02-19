import json

# 枚举定义
class NarrativeType:
    EMOTIONAL = "情绪叙事"
    EVIDENCE = "证据叙事"
    LEGAL = "法律叙事"

# Mock 分类函数
def classify_text(text: str) -> dict:
    emotional_keywords = ["可怜", "害怕", "失去", "妈妈"]
    evidence_keywords = ["证据", "聊天记录", "现场", "表明"]
    legal_keywords = ["法院", "判决", "刑事责任", "民事赔偿"]
    
    emotional_score = sum(1 for keyword in emotional_keywords if keyword in text)
    evidence_score = sum(1 for keyword in evidence_keywords if keyword in text)
    legal_score = sum(1 for keyword in legal_keywords if keyword in text)
    
    scores = {
        "EMOTIONAL": emotional_score,
        "EVIDENCE": evidence_score,
        "LEGAL": legal_score
    }
    
    max_score = max(scores.values())
    if max_score == 0:
        return {"label": "EMOTIONAL", "confidence": 0.5}
    
    label = max(scores, key=scores.get)
    total_score = sum(scores.values())
    confidence = max_score / total_score
    
    return {"label": label, "confidence": confidence}

# 分析函数
def analyse_text_entry(entry: dict) -> dict:
    result = classify_text(entry["text"])
    label_map = {
        "EMOTIONAL": NarrativeType.EMOTIONAL,
        "EVIDENCE": NarrativeType.EVIDENCE,
        "LEGAL": NarrativeType.LEGAL
    }
    return {
        "time": entry["time"],
        "text": entry["text"],
        "narrative": label_map[result["label"]],
        "confidence": result["confidence"]
    }

# 构建时间轴函数
def build_timeline(analysed_entries: list) -> list:
    return sorted(analysed_entries, key=lambda x: x["time"])

# 显示时间轴函数
def display_timeline(timeline_data: list):
    print("=" * 80)
    print("刘鑫江歌案 - 叙事类型演化时间轴")
    print("=" * 80)
    
    for entry in timeline_data:
        time = entry["time"]
        text = entry["text"]
        narrative = entry["narrative"]
        confidence = entry["confidence"]
        
        print(f"时间: {time}")
        print(f"文本: {text}")
        print(f"叙事类型: {narrative} (置信度: {confidence:.2f})")
        print("-" * 80)
    
    print("=" * 80)

# 主函数
def main():
    try:
        # 读取原始文本数据
        with open("data/raw_texts.json", "r", encoding="utf-8") as f:
            raw_entries = json.load(f)
        
        print("读取到的原始数据:")
        for entry in raw_entries:
            print(f"{entry['time']}: {entry['text']}")
        print()
        
        # 分析每个文本条目
        analysed_entries = []
        for entry in raw_entries:
            analysed_entry = analyse_text_entry(entry)
            analysed_entries.append(analysed_entry)
        
        # 构建时间轴
        timeline = build_timeline(analysed_entries)
        
        # 显示时间轴
        display_timeline(timeline)
        
        print("测试完成！")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
