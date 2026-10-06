from .config import CRYPTO_PAY_TOKEN, CRYPTO_ASSET, CRYPTO_TESTNET
import aiohttp, uuid

class CryptoBot:
    def __init__(self):
        self.base="https://testnet-pay.crypt.bot/api" if CRYPTO_TESTNET else "https://pay.crypt.bot/api"

    async def call(self,method,data):
        if not CRYPTO_PAY_TOKEN: raise RuntimeError("CryptoBot token не задан")
        async with aiohttp.ClientSession() as s:
            async with s.post(self.base+"/"+method,headers={"Crypto-Pay-API-Token":CRYPTO_PAY_TOKEN},json=data) as r:
                obj=await r.json()
                if not obj.get("ok"): raise RuntimeError(str(obj))
                return obj["result"]

    async def invoice(self,amount,description):
        return await self.call("createInvoice",{"currencyType":"fiat","fiat":"RUB","amount":str(amount),
            "description":description,"payload":str(uuid.uuid4())})

class Platega:
    """Adapter placeholder. Add credentials and exact API mapping when Platega account is ready."""
    async def create_invoice(self,*args,**kwargs):
        raise RuntimeError("Platega пока не настроена")

async def stars_price(rub):
    # Telegram Stars pricing is configured here later according to the chosen RUB/Stars policy.
    return max(1, round(rub))
