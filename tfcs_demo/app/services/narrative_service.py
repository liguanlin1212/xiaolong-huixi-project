from ai.inference.npu_runner import classify_text
from core.enums import NarrativeType

def analyse_text_entry(entry: dict) -> dict:
    result = classify_text(entry["text"])
    return {
        "time": entry["time"],
        "text": entry["text"],
        "narrative": NarrativeType[result["label"]],
        "confidence": result["confidence"]
    }
