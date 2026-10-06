import aiosqlite, os
from datetime import datetime, timezone, timedelta
from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY,
 username TEXT,
 expires_at TEXT,
 devices INTEGER NOT NULL DEFAULT 1,
 referred_by INTEGER,
 referrals INTEGER NOT NULL DEFAULT 0,
 paid_referrals INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS node_clients(
 user_id INTEGER,
 node TEXT,
 client_name TEXT,
 link TEXT,
 PRIMARY KEY(user_id,node)
);
CREATE TABLE IF NOT EXISTS promo_codes(
 code TEXT PRIMARY KEY,
 days INTEGER NOT NULL,
 uses_left INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS promo_uses(
 user_id INTEGER,
 code TEXT,
 PRIMARY KEY(user_id,code)
);
CREATE TABLE IF NOT EXISTS payments(
 id TEXT PRIMARY KEY,
 user_id INTEGER NOT NULL,
 provider TEXT NOT NULL,
 amount INTEGER NOT NULL,
 plan TEXT NOT NULL,
 devices INTEGER NOT NULL,
 status TEXT NOT NULL DEFAULT 'pending'
);
"""

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()

async def ensure_user(uid, username=None, ref=None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur=await db.execute("SELECT id FROM users WHERE id=?",(uid,))
        row=await cur.fetchone()
        if not row:
            await db.execute("INSERT INTO users(id,username,referred_by) VALUES(?,?,?)",(uid,username,ref))
        else:
            await db.execute("UPDATE users SET username=? WHERE id=?",(username,uid))
        await db.commit()

async def get_user(uid):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory=aiosqlite.Row
        cur=await db.execute("SELECT * FROM users WHERE id=?",(uid,))
        return await cur.fetchone()

async def set_expiry(uid, days):
    now=datetime.now(timezone.utc)
    async with aiosqlite.connect(DB_PATH) as db:
        cur=await db.execute("SELECT expires_at FROM users WHERE id=?",(uid,))
        row=await cur.fetchone()
        old=datetime.fromisoformat(row[0]) if row and row[0] else now
        if old < now: old=now
        new=old+timedelta(days=days)
        await db.execute("UPDATE users SET expires_at=? WHERE id=?",(new.isoformat(),uid))
        await db.commit()
        return new

async def set_devices(uid, devices):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET devices=? WHERE id=?",(devices,uid))
        await db.commit()

async def save_node_client(uid,node,name,link):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT INTO node_clients(user_id,node,client_name,link)
        VALUES(?,?,?,?) ON CONFLICT(user_id,node) DO UPDATE SET client_name=excluded.client_name,link=excluded.link""",
        (uid,node,name,link))
        await db.commit()

async def get_node_clients(uid):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory=aiosqlite.Row
        cur=await db.execute("SELECT * FROM node_clients WHERE user_id=? ORDER BY node",(uid,))
        return await cur.fetchall()

async def promo_use(uid,code):
    async with aiosqlite.connect(DB_PATH) as db:
        cur=await db.execute("SELECT days,uses_left FROM promo_codes WHERE code=?",(code,))
        row=await cur.fetchone()
        if not row or row[1] <= 0: return None
        cur=await db.execute("SELECT 1 FROM promo_uses WHERE user_id=? AND code=?",(uid,code))
        if await cur.fetchone(): return None
        await db.execute("UPDATE promo_codes SET uses_left=uses_left-1 WHERE code=?",(code,))
        await db.execute("INSERT INTO promo_uses(user_id,code) VALUES(?,?)",(uid,code))
        await db.commit()
        return row[0]
