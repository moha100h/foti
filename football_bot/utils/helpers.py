def confidence_emoji(conf: float) -> str:
    if conf >= 0.8: return "🟢"
    elif conf >= 0.6: return "🟡"
    return "🔴"

def format_percent(val: float) -> str:
    return f"{val * 100:.1f}%"
