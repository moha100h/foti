"""Advanced engine: Dixon-Coles bivariate Poisson + time-decay + Elo blend."""
import math
from datetime import datetime, timezone
from typing import List, Dict

ELO_BASE = 1500.0
ELO_K = 24.0

def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None

def _decay_weight(match_dt, half_life_days):
    if not match_dt:
        return 1.0
    now = datetime.now(timezone.utc)
    if match_dt.tzinfo is None:
        match_dt = match_dt.replace(tzinfo=timezone.utc)
    age = max(0.0, (now - match_dt).total_seconds() / 86400.0)
    return 0.5 ** (age / max(1.0, half_life_days))

def _ee(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def build_elo(fin):
    r = {}
    for m in sorted(fin, key=lambda x: x.get("utc_date", "")):
        h, a = m.get("home"), m.get("away")
        if not h or not a:
            continue
        rh = r.get(h, ELO_BASE); ra = r.get(a, ELO_BASE)
        eh = _ee(rh + 60, ra)
        hs = m.get("home_score", 0) or 0; as_ = m.get("away_score", 0) or 0
        sh = 1.0 if hs > as_ else (0.0 if hs < as_ else 0.5)
        mult = math.log(abs(hs - as_) + 1) + 1
        r[h] = rh + ELO_K * mult * (sh - eh)
        r[a] = ra + ELO_K * mult * ((1 - sh) - (1 - eh))
    return r

def _weighted_rates(fin, half_life, league_avg):
    atk_h = {}; dfn_h = {}; atk_a = {}; dfn_a = {}; wsum = {}
    for m in fin:
        h, a = m.get("home"), m.get("away")
        if not h or not a:
            continue
        w = _decay_weight(_parse_dt(m.get("utc_date")), half_life)
        hs = m.get("home_score", 0) or 0; as_ = m.get("away_score", 0) or 0
        atk_h.setdefault(h, [0.0, 0.0]); dfn_h.setdefault(h, [0.0, 0.0])
        atk_a.setdefault(a, [0.0, 0.0]); dfn_a.setdefault(a, [0.0, 0.0])
        atk_h[h][0] += hs * w; atk_h[h][1] += w
        dfn_h[h][0] += as_ * w; dfn_h[h][1] += w
        atk_a[a][0] += as_ * w; atk_a[a][1] += w
        dfn_a[a][0] += hs * w; dfn_a[a][1] += w
        wsum[h] = wsum.get(h, 0) + w; wsum[a] = wsum.get(a, 0) + w
    teams = set(list(atk_h) + list(atk_a) + list(dfn_h) + list(dfn_a))
    rates = {}
    for t in teams:
        ah = atk_h.get(t, [0, 0]); dh = dfn_h.get(t, [0, 0])
        aa = atk_a.get(t, [0, 0]); da = dfn_a.get(t, [0, 0])
        rates[t] = {
            "atk_home": max(0.25, (ah[0] / ah[1] / league_avg) if ah[1] else 1.0),
            "dfn_home": max(0.25, (dh[0] / dh[1] / league_avg) if dh[1] else 1.0),
            "atk_away": max(0.25, (aa[0] / aa[1] / league_avg) if aa[1] else 1.0),
            "dfn_away": max(0.25, (da[0] / da[1] / league_avg) if da[1] else 1.0),
            "samples": wsum.get(t, 0),
        }
    return rates

def _pois(k, l):
    return (l ** k) * math.exp(-l) / math.factorial(k)

def _dc_tau(i, j, lh, la, rho):
    if i == 0 and j == 0:
        return 1 - lh * la * rho
    if i == 0 and j == 1:
        return 1 + lh * rho
    if i == 1 and j == 0:
        return 1 + la * rho
    if i == 1 and j == 1:
        return 1 - rho
    return 1.0

def predict_match(home, away, rates, elo, *, home_adv, league_avg, rho, elo_weight):
    rh = rates.get(home); ra = rates.get(away)
    if rh:
        lh = max(0.12, rh["atk_home"] * (ra["dfn_away"] if ra else 1.0) * league_avg * home_adv)
    else:
        lh = league_avg * home_adv
    if ra:
        la = max(0.12, ra["atk_away"] * (rh["dfn_home"] if rh else 1.0) * league_avg)
    else:
        la = league_avg
    eh = _ee(elo.get(home, ELO_BASE) + 60, elo.get(away, ELO_BASE))
    mg = 10
    mat = [[_pois(i, lh) * _pois(j, la) * _dc_tau(i, j, lh, la, rho) for j in range(mg + 1)] for i in range(mg + 1)]
    s = sum(sum(row) for row in mat)
    if s > 0:
        mat = [[v / s for v in row] for row in mat]
    ph = pd = pa = po = pb = 0.0
    for i in range(mg + 1):
        for j in range(mg + 1):
            p = mat[i][j]
            if i > j: ph += p
            elif i == j: pd += p
            else: pa += p
            if i + j > 2: po += p
            if i >= 1 and j >= 1: pb += p
    eh_h = eh * (1 - pd); eh_a = (1 - eh) * (1 - pd)
    ph = (1 - elo_weight) * ph + elo_weight * eh_h
    pa = (1 - elo_weight) * pa + elo_weight * eh_a
    tot = ph + pd + pa
    ph, pd, pa = ph / tot, pd / tot, pa / tot
    oc = sorted([("home", ph), ("draw", pd), ("away", pa)], key=lambda x: x[1], reverse=True)
    best, bp = oc[0]
    flat = sorted(((i, j, mat[i][j]) for i in range(mg + 1) for j in range(mg + 1)), key=lambda x: x[2], reverse=True)
    ls = flat[0]
    samples = (rh["samples"] if rh else 0) + (ra["samples"] if ra else 0)
    risk = "low" if (bp >= 0.6 and samples >= 8) else ("medium" if bp >= 0.45 else "high")
    return {"home": home, "away": away, "winner": best,
            "winner_name": home if best == "home" else (away if best == "away" else "draw"),
            "p_home": round(ph, 4), "p_draw": round(pd, 4), "p_away": round(pa, 4),
            "p_over25": round(po, 4), "p_under25": round(1 - po, 4), "p_btts": round(pb, 4),
            "xg_home": round(lh, 2), "xg_away": round(la, 2), "likely_score": f"{ls[0]}-{ls[1]}",
            "confidence": round(bp, 4), "risk_level": risk, "samples": int(samples)}

def predict_fixtures(up, fin, *, home_adv=1.35, league_avg=1.35, rho=-0.08, elo_weight=0.30, half_life=120.0):
    rates = _weighted_rates(fin, half_life, league_avg)
    elo = build_elo(fin)
    out = []
    for m in up:
        h, a = m.get("home"), m.get("away")
        if not h or not a:
            continue
        p = predict_match(h, a, rates, elo, home_adv=home_adv, league_avg=league_avg, rho=rho, elo_weight=elo_weight)
        p["utc_date"] = m.get("utc_date", ""); p["league"] = m.get("league", "")
        out.append(p)
    out.sort(key=lambda x: x["confidence"], reverse=True)
    return out
