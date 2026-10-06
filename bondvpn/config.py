import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def b(name, default="false"):
    return os.getenv(name, default).lower() in {"1","true","yes","on"}

def ints(name):
    return {int(x.strip()) for x in os.getenv(name, "").split(",") if x.strip().isdigit()}

@dataclass
class Node:
    key: str
    title: str
    flag: str
    url: str
    token: str

NODES = [
    Node("usa","США","🇺🇸",os.getenv("H1_USA_URL",""),os.getenv("H1_USA_TOKEN","")),
    Node("germany","Германия","🇩🇪",os.getenv("H1_GERMANY_URL",""),os.getenv("H1_GERMANY_TOKEN","")),
    Node("spain","Испания","🇪🇸",os.getenv("H1_SPAIN_URL",""),os.getenv("H1_SPAIN_TOKEN","")),
    Node("poland","Польша","🇵🇱",os.getenv("H1_POLAND_URL",""),os.getenv("H1_POLAND_TOKEN","")),
    Node("lithuania","Литва","🇱🇹",os.getenv("H1_LITHUANIA_URL",""),os.getenv("H1_LITHUANIA_TOKEN","")),
]

PLANS = {
    "1m": ("1 месяц", 30, int(os.getenv("PRICE_1M","118"))),
    "3m": ("3 месяца", 90, int(os.getenv("PRICE_3M","318"))),
    "6m": ("6 месяцев", 180, int(os.getenv("PRICE_6M","618"))),
    "12m": ("1 год", 365, int(os.getenv("PRICE_12M","1418"))),
}

BOT_TOKEN=os.getenv("BOT_TOKEN","")
ADMIN_IDS=ints("ADMIN_IDS")
DB_PATH=os.getenv("DB_PATH","./data/bondvpn.db")
INCLUDED_DEVICES=int(os.getenv("INCLUDED_DEVICES","1"))
EXTRA_DEVICE_PRICE=int(os.getenv("EXTRA_DEVICE_PRICE","10"))
SUPPORT_USERNAME=os.getenv("SUPPORT_USERNAME","Razzy016").lstrip("@")
SECOND_ADMIN_USERNAME=os.getenv("SECOND_ADMIN_USERNAME","Tioma_bond").lstrip("@")
STARS_ENABLED=b("STARS_ENABLED","true")
CRYPTO_ENABLED=b("CRYPTO_ENABLED","true")
CRYPTO_PAY_TOKEN=os.getenv("CRYPTO_PAY_TOKEN","")
CRYPTO_ASSET=os.getenv("CRYPTO_ASSET","USDT")
CRYPTO_TESTNET=b("CRYPTO_TESTNET","false")
PLATEGA_ENABLED=b("PLATEGA_ENABLED","false")
REFERRAL_DAYS_INVITER=int(os.getenv("REFERRAL_DAYS_INVITER","7"))
REFERRAL_DAYS_FRIEND=int(os.getenv("REFERRAL_DAYS_FRIEND","3"))
H1_VERIFY_SSL=b("H1_VERIFY_SSL","false")
