from typing import Dict, Any

def format_live_match(m: Dict[str, Any]) -> str:
    minute = m.get("minute", "")
    min_str = f" {minute}'" if minute else ""
    return (f"<b>{m.get('home','')} {m.get('home_score','?')} - {m.get('away_score','?')} {m.get('away','')}</b>
"
            f"   {m.get('league','')} | {m.get('status','')}{min_str}
")

def format_fixture(m: Dict[str, Any]) -> str:
    return f"{m.get('time','')} | <b>{m.get('home','')} vs {m.get('away','')}</b>
   {m.get('league','')}
"

def format_prediction(p: Any) -> str:
    conf = int((p.confidence or 0) * 100)
    risk_map = {"low": "پایین", "medium": "متوسط", "high": "بالا"}
    risk = risk_map.get(p.risk_level or "medium", "متوسط")
    text = f"<b>نوع:</b> {p.prediction_type}
<b>اطمینان:</b> {conf}%
<b>ریسک:</b> {risk}
"
    if p.explanation:
        text += f"<i>{p.explanation}</i>
"
    return text

def format_wc_match(m: Dict[str, Any]) -> str:
    return f"<b>{m.get('home','')} vs {m.get('away','')}</b>
   {m.get('time','')} | گروه {m.get('group','')}
"
