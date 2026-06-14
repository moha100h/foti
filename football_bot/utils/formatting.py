"""Persian-safe rendering."""
FA = {
    "live_title": "\U0001f534 <b>\u0646\u062a\u0627\u06cc\u062c \u0632\u0646\u062f\u0647</b>\n\n",
    "no_live": "\u0627\u06a9\u0646\u0648\u0646 \u0628\u0627\u0632\u06cc \u0632\u0646\u062f\u0647\u200c\u0627\u06cc \u062f\u0631 \u062c\u0631\u06cc\u0627\u0646 \u0646\u06cc\u0633\u062a.",
    "goal": "\u06af\u0644", "points": "\u0627\u0645\u062a\u06cc\u0627\u0632",
    "winner": "\u0628\u0631\u0646\u062f\u0647 \u0627\u062d\u062a\u0645\u0627\u0644\u06cc", "draw": "\u0645\u0633\u0627\u0648\u06cc",
    "likely": "\u0646\u062a\u06cc\u062c\u0647 \u0645\u062d\u062a\u0645\u0644",
    "over": "\u0628\u0627\u0644\u0627\u06cc \u06f2.\u06f5", "btts": "\u0647\u0631\u062f\u0648 \u06af\u0644",
}

def fmt_live(m):
    mn = m.get("minute","")
    mns = f"  {mn}'" if mn else ""
    return f"<b>{m['home']} {m['home_score']} - {m['away_score']} {m['away']}</b>\n   {m.get('league','')}{mns}\n"

def fmt_fixture(m):
    t = (m.get("utc_date","") or "")[11:16]
    return f"{t}  <b>{m['home']}</b> vs <b>{m['away']}</b>\n   {m.get('league','')}\n"

def fmt_prediction(p):
    conf = int(round(p["confidence"]*100))
    wn = FA["draw"] if p["winner"]=="draw" else p["winner_name"]
    return ("\n".join([
        f"<b>{p['home']} \u2014 {p['away']}</b>",
        f"   \U0001f3c6 {FA['winner']}: <b>{wn}</b> ({conf}%)",
        f"   \U0001f4ca 1: {int(p['p_home']*100)}%  X: {int(p['p_draw']*100)}%  2: {int(p['p_away']*100)}%",
        f"   \u26bd {FA['likely']}: <b>{p['likely_score']}</b>  (xG {p['xg_home']}-{p['xg_away']})",
        f"   \U0001f4c8 {FA['over']}: {int(p['p_over25']*100)}%  |  {FA['btts']}: {int(p['p_btts']*100)}%",
    ]) + "\n")

def fmt_scorer(i, s):
    return f"{i}. <b>{s['name']}</b> ({s['team']}) \u2014 {s['goals']} {FA['goal']}\n"

def fmt_table_row(t):
    return f"{t['position']}. <b>{t['team']}</b> \u2014 {t['points']} {FA['points']} ({t['played']})\n"
