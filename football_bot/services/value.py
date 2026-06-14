"""Value-betting layer: fetch bookmaker odds, compute edge & Kelly stake."""
import aiohttp
from typing import List, Dict
from loguru import logger

async def fetch_odds(api_key: str, sport: str = "soccer", regions: str = "eu") -> List[Dict]:
    if not api_key:
        return []
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {"apiKey": api_key, "regions": regions, "markets": "h2h", "oddsFormat": "decimal"}
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=12)) as s:
            async with s.get(url, params=params) as r:
                if r.status == 200:
                    return await r.json(content_type=None)
                logger.warning(f"odds API HTTP {r.status}")
    except Exception as e:
        logger.error(f"odds fetch failed: {e}")
    return []

def _norm(s: str) -> str:
    return (s or "").lower().replace("fc", "").replace(".", "").strip()

def _best_h2h(event: Dict):
    home = event.get("home_team", ""); away = event.get("away_team", "")
    best = {"home": 0.0, "draw": 0.0, "away": 0.0}
    for bk in event.get("bookmakers", []):
        for mk in bk.get("markets", []):
            if mk.get("key") != "h2h":
                continue
            for o in mk.get("outcomes", []):
                name = o.get("name", ""); price = o.get("price", 0) or 0
                if _norm(name) == _norm(home):
                    best["home"] = max(best["home"], price)
                elif _norm(name) == _norm(away):
                    best["away"] = max(best["away"], price)
                elif name.lower() == "draw":
                    best["draw"] = max(best["draw"], price)
    return home, away, best

def kelly_fraction(prob: float, odds: float, cap: float = 0.25) -> float:
    b = odds - 1.0
    if b <= 0:
        return 0.0
    f = (prob * odds - 1.0) / b
    return max(0.0, min(cap, f))

def find_value_bets(predictions: List[Dict], odds_events: List[Dict], *,
                    min_edge: float = 0.05, kelly_cap: float = 0.25,
                    kelly_mult: float = 0.5) -> List[Dict]:
    out = []
    for ev in odds_events:
        home, away, best = _best_h2h(ev)
        pred = next((p for p in predictions
                     if _norm(p["home"]) == _norm(home) and _norm(p["away"]) == _norm(away)), None)
        if not pred:
            continue
        for sel, prob, odd in (("home", pred["p_home"], best["home"]),
                               ("draw", pred["p_draw"], best["draw"]),
                               ("away", pred["p_away"], best["away"])):
            if odd <= 1.01:
                continue
            edge = prob * odd - 1.0
            if edge < min_edge:
                continue
            stake = kelly_fraction(prob, odd, kelly_cap) * kelly_mult
            label = home if sel == "home" else (away if sel == "away" else "Draw")
            out.append({"home": home, "away": away, "selection": sel, "selection_name": label,
                        "prob": round(prob, 4), "odds": round(odd, 2), "edge": round(edge, 4),
                        "kelly_stake_pct": round(stake * 100, 2),
                        "fair_odds": round(1.0 / prob, 2) if prob > 0 else 0.0,
                        "league": pred.get("league", ""), "utc_date": pred.get("utc_date", "")})
    out.sort(key=lambda x: x["edge"], reverse=True)
    return out
