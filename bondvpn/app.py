import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice
from .config import *
from . import db
from .keyboards import main, plans, back, pay
from .vpn import provision, renew
from .payments import CryptoBot, Platega

bot=None

async def start(m:Message):
    ref=None
    parts=(m.text or "").split(maxsplit=1)
    if len(parts)==2 and parts[1].startswith("ref_"):
        try: ref=int(parts[1][4:])
        except: pass
    await db.ensure_user(m.from_user.id,m.from_user.username,ref)
    await m.answer(
        "🟦 <b>BOND VPN</b>\n\n"
        "Быстрый и стабильный VPN.\n"
        "Одна подписка → 🇺🇸 🇩🇪 🇪🇸 🇵🇱 🇱🇹\n\n"
        "Выберите действие:",
        reply_markup=main(),parse_mode="HTML")

async def home(c:CallbackQuery):
    await c.message.edit_text("🟦 <b>BOND VPN</b>\n\nВыберите действие:",reply_markup=main(),parse_mode="HTML")
    await c.answer()

async def subscription(c):
    u=await db.get_user(c.from_user.id)
    if not u or not u["expires_at"]:
        txt="👤 <b>Моя подписка</b>\n\n❌ Активной подписки нет."
    else:
        txt=f"👤 <b>Моя подписка</b>\n\nСтатус: {'🟢 Активна' if u['expires_at'] else '🔴 Нет'}\nДо: <b>{u['expires_at'][:10]}</b>\nУстройств: <b>{u['devices']}</b>\n\nДоступны все 5 серверов."
    await c.message.edit_text(txt,reply_markup=back(),parse_mode="HTML"); await c.answer()

async def connect(c):
    rows=await db.get_node_clients(c.from_user.id)
    if not rows:
        await c.message.edit_text("⚡ <b>Подключиться</b>\n\nСначала приобретите подписку.",reply_markup=back(),parse_mode="HTML")
    else:
        lines=["⚡ <b>Подключение BOND VPN</b>",""]
        for r in rows:
            lines.append(f"<b>{r['node'].upper()}</b>\n<code>{r['link'] or 'ссылка пока не получена'}</code>\n")
        await c.message.edit_text("\n".join(lines),reply_markup=back(),parse_mode="HTML")
    await c.answer()

async def shop(c):
    await c.message.edit_text("🛒 <b>Магазин</b>\n\nВыберите срок подписки:",reply_markup=plans(),parse_mode="HTML"); await c.answer()

async def plan(c):
    p=c.data.split(":")[1]
    title,days,price=PLANS[p]
    await c.message.edit_text(f"🛒 <b>{title}</b>\n\nЦена: <b>{price} ₽</b>\nВключено устройств: <b>{INCLUDED_DEVICES}</b>\nДоп. устройство: <b>+{EXTRA_DEVICE_PRICE} ₽</b>",reply_markup=pay(p),parse_mode="HTML"); await c.answer()

async def pay_start(c):
    _,provider,p=c.data.split(":")
    title,days,price=PLANS[p]
    if provider=="crypto":
        try:
            inv=await CryptoBot().invoice(price,f"BOND VPN — {title}")
            await c.message.edit_text(f"🪙 <b>CryptoBot</b>\n\nОплатите счёт: {inv.get('pay_url','')}",reply_markup=back(),parse_mode="HTML")
        except Exception as e:
            await c.message.edit_text(f"❌ CryptoBot пока не настроен.",reply_markup=back())
    elif provider=="platega":
        await c.message.edit_text("💳 Platega пока подключается. После выдачи API-данных этот способ включится.",reply_markup=back())
    else:
        await c.message.edit_text("⭐ Telegram Stars: платёжный модуль подготовлен; перед запуском нужно задать курс RUB → Stars.",reply_markup=back())
    await c.answer()

async def promo(c):
    await c.message.edit_text("🎟 <b>Промокод</b>\n\nОтправьте промокод отдельным сообщением после нажатия /promo CODE.",reply_markup=back(),parse_mode="HTML"); await c.answer()

async def promo_cmd(m):
    parts=(m.text or "").split(maxsplit=1)
    if len(parts)!=2:
        await m.answer("Использование: /promo CODE"); return
    days=await db.promo_use(m.from_user.id,parts[1].strip().upper())
    if days is None: await m.answer("❌ Промокод недействителен.")
    else:
        await db.set_expiry(m.from_user.id,days)
        await m.answer(f"🎉 Промокод активирован! +{days} дней.")

async def about(c):
    await c.message.edit_text(f"ℹ️ <b>О BOND VPN</b>\n\n5 локаций в одной подписке.\nПоддержка: @{SUPPORT_USERNAME}\nАдминистратор: @{SECOND_ADMIN_USERNAME}",reply_markup=back(),parse_mode="HTML"); await c.answer()

async def ref(c):
    me=await bot.get_me()
    link=f"https://t.me/{me.username}?start=ref_{c.from_user.id}"
    await c.message.edit_text(f"🎁 <b>Реферальная программа</b>\n\nДруг получает +3 дня.\nВы получаете +7 дней после его оплаты.\n\nВаша ссылка:\n<code>{link}</code>",reply_markup=back(),parse_mode="HTML"); await c.answer()

async def myid(m):
    await m.answer(f"Ваш Telegram ID: <code>{m.from_user.id}</code>",parse_mode="HTML")

async def main():
    global bot
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан. Заполните .env")
    await db.init_db()
    bot=Bot(BOT_TOKEN)
    dp=Dispatcher()
    dp.message.register(start,CommandStart())
    dp.message.register(myid,Command("myid"))
    dp.message.register(promo_cmd,Command("promo"))
    dp.callback_query.register(home,F.data=="home")
    dp.callback_query.register(subscription,F.data=="sub")
    dp.callback_query.register(connect,F.data=="connect")
    dp.callback_query.register(shop,F.data=="shop")
    dp.callback_query.register(promo,F.data=="promo")
    dp.callback_query.register(ref,F.data=="ref")
    dp.callback_query.register(about,F.data=="about")
    dp.callback_query.register(plan,F.data.startswith("plan:"))
    dp.callback_query.register(pay_start,F.data.startswith("pay:"))
    await dp.start_polling(bot)
