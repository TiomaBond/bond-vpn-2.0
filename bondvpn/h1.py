import aiohttp
from .config import H1_VERIFY_SSL, Node

class H1Client:
    def __init__(self,node:Node):
        self.node=node

    @property
    def enabled(self):
        return bool(self.node.url and self.node.token)

    def headers(self):
        return {"Authorization":f"Bearer {self.node.token}","Content-Type":"application/json"}

    async def request(self,method,path,**kwargs):
        if not self.enabled:
            raise RuntimeError(f"{self.node.title}: API не настроен")
        timeout=aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.request(method,self.node.url.rstrip("/")+"/"+path.lstrip("/"),
                                  headers=self.headers(),ssl=H1_VERIFY_SSL,**kwargs) as r:
                text=await r.text()
                if r.status >= 400:
                    raise RuntimeError(f"H1 {self.node.title}: HTTP {r.status}: {text[:300]}")
                try: return await r.json()
                except: return {"raw":text}

    async def health(self):
        return await self.request("GET","/health")

    async def create(self,name,days,devices):
        # H1Cloud reference API: POST /create
        return await self.request("POST","/create",json={
            "name":name,"days":days,"devices":devices
        })

    async def edit(self,name,days=None,devices=None):
        body={"name":name}
        if days is not None: body["days"]=days
        if devices is not None: body["devices"]=devices
        return await self.request("PATCH","/edit",json=body)

    async def client(self,name):
        return await self.request("GET",f"/clients/{name}")
