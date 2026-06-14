"""Hybrid Poisson + Elo engine -> 1X2 / Over-Under 2.5 / BTTS / likely score."""
import math
from typing import List, Dict

HOME_ADV = 0.35
AVG = 1.35
ELO_BASE = 1500.0
ELO_K = 24.0

def _ee(ra, rb): return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def build_elo(fin):
    r = {}
    for m in fin:
        h, a = m.get("home"), m.get("away")
        if not h or not a: continue
        rh = r.get(h, ELO_BASE); ra = r.get(a, ELO_BASE)
        eh = _ee(rh + 60, ra)
        hs = m.get("home_score",0) or 0; as_ = m.get("away_score",0) or 0
        sh = 1.0 if hs > as_ else (0.0 if hs < as_ else 0.5)
        mult = math.log(abs(hs - as_) + 1) + 1
        r[h] = rh + ELO_K * mult * (sh - eh)
        r[a] = ra + ELO_K * mult * ((1 - sh) - (1 - eh))
    return r

def _rates(fin):
    sc = {}; cc = {}
    for m in fin:
        h, a = m.get("home"), m.get("away")
        if not h or not a: continue
        hs = m.get("home_score",0) or 0; as_ = m.get("away_score",0) or 0
        sc.setdefault(h, []).append(hs); sc.setdefault(a, []).append(as_)
        cc.setdefault(h, []).append(as_); cc.setdefault(a, []).append(hs)
    out = {}
    for t in set(list(sc) + list(cc)):
        s = sc.get(t, []); c = cc.get(t, [])
        atk = (sum(s)/len(s))/AVG if s else 1.0
        dfn = (sum(c)/len(c))/AVG if c else 1.0
        out[t] = {"attack": max(0.3, atk), "defense": max(0.3, dfn)}
    return out

def _pois(k, l): return (l ** k) * math.exp(-l) / math.factorial(k)

def predict_match(home, away, rates, elo):
    rh = rates.get(home, {"attack":1.0,"defense":1.0}); ra = rates.get(away, {"attack":1.0,"defense":1.0})
    lh = max(0.15, rh["attack"] * ra["defense"] * AVG + HOME_ADV)
    la = max(0.15, ra["attack"] * rh["defense"] * AVG)
    eh = _ee(elo.get(home, ELO_BASE) + 60, elo.get(away, ELO_BASE))
    mg = 8
    mat = [[_pois(i, lh) * _pois(j, la) for j in range(mg+1)] for i in range(mg+1)]
    ph = pd = pa = po = pb = 0.0
    for i in range(mg+1):
        for j in range(mg+1):
            p = mat[i][j]
            if i > j: ph += p
            elif i == j: pd += p
            else: pa += p
            if i + j > 2: po += p
            if i >= 1 and j >= 1: pb += p
    eh_h = eh * (1 - pd); eh_a = (1 - eh) * (1 - pd)
    ph = 0.7*ph + 0.3*eh_h; pa = 0.7*pa + 0.3*eh_a
    tot = ph + pd + pa; ph, pd, pa = ph/tot, pd/tot, pa/tot
    oc = sorted([("home",ph),("draw",pd),("away",pa)], key=lambda x: x[1], reverse=True)
    best, bp = oc[0]
    flat = sorted(((i,j,mat[i][j]) for i in range(mg+1) for j in range(mg+1)), key=lambda x: x[2], reverse=True)
    ls = flat[0]
    risk = "low" if bp >= 0.6 else ("medium" if bp >= 0.45 else "high")
    return {"home": home, "away": away, "winner": best,
            "winner_name": home if best=="home" else (away if best=="away" else "draw"),
            "p_home": round(ph,3), "p_draw": round(pd,3), "p_away": round(pa,3),
            "p_over25": round(po,3), "p_under25": round(1-po,3), "p_btts": round(pb,3),
            "xg_home": round(lh,2), "xg_away": round(la,2), "likely_score": f"{ls[0]}-{ls[1]}",
            "confidence": round(bp,3), "risk_level": risk}

def predict_fixtures(up, fin):
    rates = _rates(fin); elo = build_elo(fin); out = []
    for m in up:
        h, a = m.get("home"), m.get("away")
        if not h or not a: continue
        p = predict_match(h, a, rates, elo)
        p["utc_date"] = m.get("utc_date",""); p["league"] = m.get("league","")
        out.append(p)
    out.sort(key=lambda x: x["confidence"], reverse=True)
    return out
