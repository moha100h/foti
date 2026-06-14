"""Bet tracking: record, settle, ROI stats."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import List, Dict, Optional
from football_bot.models.bet import Bet

async def record_bet(db: AsyncSession, user_id: int, vb: Dict, stake: float) -> Bet:
    bet = Bet(user_id=user_id, home=vb["home"], away=vb["away"], selection=vb["selection"],
              selection_name=vb.get("selection_name"), odds=vb["odds"], stake=stake,
              model_prob=vb.get("prob"), edge=vb.get("edge"), league=vb.get("league"))
    db.add(bet)
    await db.flush()
    return bet

async def settle_bet(db: AsyncSession, bet_id: int, result: str) -> Optional[Bet]:
    bet = await db.get(Bet, bet_id)
    if not bet or bet.result != "pending":
        return bet
    bet.result = result
    if result == "won":
        bet.profit = round(bet.stake * (bet.odds - 1.0), 2)
    elif result == "lost":
        bet.profit = round(-bet.stake, 2)
    else:
        bet.profit = 0.0
    bet.settled_at = datetime.now(timezone.utc)
    await db.flush()
    return bet

async def list_pending(db: AsyncSession, user_id: int) -> List[Bet]:
    res = await db.execute(select(Bet).where(Bet.user_id == user_id, Bet.result == "pending").order_by(Bet.created_at.desc()))
    return list(res.scalars().all())

async def stats(db: AsyncSession, user_id: int) -> Dict:
    res = await db.execute(select(Bet).where(Bet.user_id == user_id))
    bets = list(res.scalars().all())
    settled = [b for b in bets if b.result in ("won", "lost", "void")]
    won = [b for b in settled if b.result == "won"]
    staked = sum(b.stake for b in settled) or 0.0
    profit = sum(b.profit for b in settled) or 0.0
    roi = (profit / staked * 100) if staked else 0.0
    wr = (len(won) / len(settled) * 100) if settled else 0.0
    return {"total": len(bets), "pending": len([b for b in bets if b.result == "pending"]),
            "settled": len(settled), "won": len(won), "win_rate": round(wr, 1),
            "staked": round(staked, 2), "profit": round(profit, 2), "roi": round(roi, 1)}
