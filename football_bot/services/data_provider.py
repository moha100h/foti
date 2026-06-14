"""Multi-source football data provider with fallback chain + in-memory TTL cache.

API token resolution order:
  1. runtime DB setting "FOOTBALL_DATA_TOKEN" (set by admin inside the bot)
  2. settings.FOOTBALL_DATA_TOKEN (.env)
  3. none -> free tier
"""
import aiohttp, time
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
from football_bot.config import settings
from football_bot.services import settings_service

_cache: Dict[str, tuple] = {}

def _cget(k):
    it = _cache.get(k)
    if it and time.time() - it[0] < it[2]:
        return it[1]
    return None

def _cset(k, v, ttl):
    _cache[k] = (time.time(), v, ttl)

async def _get_json(url, headers=None, params=None):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=12)) as s:
            async with s.get(url, headers=headers or {}, params=params or {}) as r:
                if r.status == 200:
                    return await r.json(content_type=None)
                logger.warning(f"HTTP {r.status} -> {url}")
    except Exception as e:
        logger.error(f"req fail {url}: {e}")
    return None

def _fdh():
    tok = settings_service.cache_get("FOOTBALL_DATA_TOKEN") or getattr(settings, "FOOTBALL_DATA_TOKEN", "") or ""
    return {"X-Auth-Token": tok} if tok else {}

async def live_matches():
    c = _cget("live")
    if c is not None: return c
    out = []
    d = await _get_json("https://api.football-data.org/v4/matches", headers=_fdh(), params={"status": "LIVE"})
    if d and d.get("matches"): out = [_nfd(m) for m in d["matches"]]
    if not out:
        e = await _get_json("https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard", params={"dates": date.today().strftime("%Y%m%d")})
        if e and e.get("events"): out = [n for n in (_nes(x) for x in e["events"]) if n and n["is_live"]]
    _cset("live", out, settings.LIVE_CACHE_TTL); return out

async def fixtures(off=0):
    k = f"fix_{off}"; c = _cget(k)
    if c is not None: return c
    t = (date.today() + timedelta(days=off)).strftime("%Y-%m-%d"); out = []
    d = await _get_json("https://api.football-data.org/v4/matches", headers=_fdh(), params={"dateFrom": t, "dateTo": t})
    if d and d.get("matches"): out = [_nfd(m) for m in d["matches"]]
    if not out:
        e = await _get_json("https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard", params={"dates": t.replace("-", "")})
        if e and e.get("events"): out = [n for n in (_nes(x) for x in e["events"]) if n]
    _cset(k, out, settings.CACHE_TTL); return out

async def top_scorers(comp="PL"):
    k = f"sc_{comp}"; c = _cget(k)
    if c is not None: return c
    d = await _get_json(f"https://api.football-data.org/v4/competitions/{comp}/scorers", headers=_fdh(), params={"limit": "15"})
    out = []
    if d and d.get("scorers"):
        for s in d["scorers"]:
            out.append({"name": (s.get("player") or {}).get("name",""),
                        "team": (s.get("team") or {}).get("shortName") or (s.get("team") or {}).get("name",""),
                        "goals": s.get("goals",0) or 0, "assists": s.get("assists",0) or 0})
    _cset(k, out, settings.CACHE_TTL); return out

async def standings(comp="PL"):
    k = f"tb_{comp}"; c = _cget(k)
    if c is not None: return c
    d = await _get_json(f"https://api.football-data.org/v4/competitions/{comp}/standings", headers=_fdh())
    out = []
    if d and d.get("standings"):
        tot = next((x for x in d["standings"] if x.get("type") == "TOTAL"), d["standings"][0])
        for t in (tot.get("table") or []):
            out.append({"position": t.get("position"),
                        "team": (t.get("team") or {}).get("shortName") or (t.get("team") or {}).get("name",""),
                        "played": t.get("playedGames",0), "won": t.get("won",0), "draw": t.get("draw",0),
                        "lost": t.get("lost",0), "gd": t.get("goalDifference",0), "points": t.get("points",0),
                        "form": t.get("form","") or ""})
    _cset(k, out, settings.CACHE_TTL); return out

async def upcoming_matches(days=7):
    c = _cget("up")
    if c is not None: return c
    df = date.today().strftime("%Y-%m-%d"); dt = (date.today()+timedelta(days=days)).strftime("%Y-%m-%d")
    d = await _get_json("https://api.football-data.org/v4/matches", headers=_fdh(), params={"dateFrom": df, "dateTo": dt, "status": "SCHEDULED"})
    out = [_nfd(m) for m in (d.get("matches") if d else [])]
    _cset("up", out, settings.CACHE_TTL); return out

async def finished_matches(days_back=60):
    c = _cget("fin")
    if c is not None: return c
    df = (date.today()-timedelta(days=days_back)).strftime("%Y-%m-%d"); dt = date.today().strftime("%Y-%m-%d")
    d = await _get_json("https://api.football-data.org/v4/matches", headers=_fdh(), params={"dateFrom": df, "dateTo": dt, "status": "FINISHED"})
    out = [_nfd(m) for m in (d.get("matches") if d else [])]
    _cset("fin", out, settings.CACHE_TTL); return out

def _nfd(m):
    sc = (m.get("score") or {}).get("fullTime") or {}
    h = m.get("homeTeam") or {}; a = m.get("awayTeam") or {}
    return {"id": m.get("id"), "home": h.get("shortName") or h.get("name",""), "away": a.get("shortName") or a.get("name",""),
            "home_id": h.get("id"), "away_id": a.get("id"),
            "home_score": sc.get("home") if sc.get("home") is not None else 0,
            "away_score": sc.get("away") if sc.get("away") is not None else 0,
            "status": m.get("status",""), "league": (m.get("competition") or {}).get("name",""),
            "utc_date": m.get("utcDate",""), "minute": m.get("minute",""),
            "is_live": m.get("status") in ("IN_PLAY","PAUSED","LIVE")}

def _nes(e):
    cs = e.get("competitions") or []
    if not cs: return None
    co = cs[0].get("competitors") or []
    h = next((c for c in co if c.get("homeAway")=="home"), {}); a = next((c for c in co if c.get("homeAway")=="away"), {})
    st = (e.get("status") or {}).get("type") or {}
    return {"id": e.get("id"), "home": (h.get("team") or {}).get("shortDisplayName",""), "away": (a.get("team") or {}).get("shortDisplayName",""),
            "home_score": h.get("score","0"), "away_score": a.get("score","0"), "status": st.get("description",""),
            "league": (e.get("leagues") or [{}])[0].get("abbreviation","") if e.get("leagues") else "",
            "utc_date": e.get("date",""), "minute": (e.get("status") or {}).get("displayClock",""),
            "is_live": st.get("state")=="in"}
