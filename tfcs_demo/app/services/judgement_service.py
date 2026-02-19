def build_timeline(analysed_entries: list) -> list:
    """
    输入：按时间排序的 AnalysedEntry
    输出：时间轴结构（list）
    """
    # 确保按时间顺序排序
    sorted_entries = sorted(analysed_entries, key=lambda x: x["time"])
    return sorted_entries
