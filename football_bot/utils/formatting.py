from typing import Dict, Any


def format_live_match(m: Dict[str, Any]) -> str:
    home = m.get("home", "")
    away = m.get("away", "")
    hs = str(m.get("home_score", "?"))
    as_ = str(m.get("away_score", "?"))
    league = m.get("league", "")
    status = m.get("status", "")
    minute = m.get("minute", "")
    min_str = (" " + str(minute) + "'") if minute else ""
    line1 = "<b>" + home + " " + hs + " - " + as_ + " " + away + "</b>"
    line2 = "   " + league + " | " + status + min_str
    return line1 + "\n" + line2 + "\n"


def format_fixture(m: Dict[str, Any]) -> str:
    t = m.get("time", "")
    home = m.get("home", "")
    away = m.get("away", "")
    league = m.get("league", "")
    return t + " | <b>" + home + " vs " + away + "</b>\n   " + league + "\n"


def format_prediction(p: Any) -> str:
    conf = int((p.confidence or 0) * 100)
    risk_map = {
        "low": "\u067e\u0627\u06cc\u06cc\u0646",
        "medium": "\u0645\u062a\u0648\u0633\u0637",
        "high": "\u0628\u0627\u0644\u0627",
    }
    risk = risk_map.get(p.risk_level or "medium", "\u0645\u062a\u0648\u0633\u0637")
    ptype = p.prediction_type or ""
    lines = [
        "<b>\u0646\u0648\u0639:</b> " + ptype,
        "<b>\u0627\u0637\u0645\u06cc\u0646\u0627\u0646:</b> " + str(conf) + "%",
        "<b>\u0631\u06cc\u0633\u06a9:</b> " + risk,
    ]
    if p.explanation:
        lines.append("<i>" + p.explanation + "</i>")
    return "\n".join(lines) + "\n"


def format_wc_match(m: Dict[str, Any]) -> str:
    home = m.get("home", "")
    away = m.get("away", "")
    t = m.get("time", "")
    group = m.get("group", "")
    return "<b>" + home + " vs " + away + "</b>\n   " + t + " | \u06af\u0631\u0648\u0647 " + group + "\n"
