def confidence_emoji(conf: float) -> str:
    if conf >= 0.8:
        return "\U0001f7e2"
    elif conf >= 0.6:
        return "\U0001f7e1"
    return "\U0001f534"


def format_percent(val: float) -> str:
    return str(round(val * 100, 1)) + "%"
