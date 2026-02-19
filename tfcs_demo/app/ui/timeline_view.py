def display_timeline(timeline_data: list):
    """
    显示时间轴
    输入：时间轴数据列表
    """
    print("=" * 80)
    print("刘鑫江歌案 - 叙事类型演化时间轴")
    print("=" * 80)
    
    for entry in timeline_data:
        time = entry["time"]
        text = entry["text"]
        narrative = entry["narrative"].value
        confidence = entry["confidence"]
        
        print(f"时间: {time}")
        print(f"文本: {text}")
        print(f"叙事类型: {narrative} (置信度: {confidence:.2f})")
        print("-" * 80)
    
    print("=" * 80)
