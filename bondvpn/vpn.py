import re
from .config import NODES
from .h1 import H1Client
from .db import save_node_client, get_node_clients

def safe_name(uid):
    return f"tg{uid}"

def extract_link(data):
    if isinstance(data,dict):
        if data.get("link"): return data["link"]
        if data.get("links") and isinstance(data["links"],list): return data["links"][0]
        for v in data.values():
            x=extract_link(v)
            if x: return x
    if isinstance(data,list):
        for v in data:
            x=extract_link(v)
            if x: return x
    return ""

async def provision(uid,days,devices):
    name=safe_name(uid)
    out=[]
    for node in NODES:
        if not node.url or not node.token:
            continue
        api=H1Client(node)
        try:
            data=await api.create(name,days,devices)
        except Exception:
            data=await api.edit(name,days=days,devices=devices)
        info=await api.client(name)
        link=extract_link(info) or extract_link(data)
        await save_node_client(uid,node.key,name,link)
        out.append((node,link))
    if not out:
        raise RuntimeError("Нет настроенных H1-нoд.")
    return out

async def renew(uid,days,devices=None):
    rows=await get_node_clients(uid)
    by={n.key:n for n in NODES}
    out=[]
    for row in rows:
        node=by.get(row["node"])
        if not node or not node.url or not node.token: continue
        info=await H1Client(node).edit(row["client_name"],days=days,devices=devices)
        link=extract_link(info)
        if link:
            await save_node_client(uid,node.key,row["client_name"],link)
        out.append((node,link or row["link"]))
    return out
