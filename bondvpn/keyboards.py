from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Моя подписка",callback_data="sub"),
         InlineKeyboardButton(text="⚡ Подключиться",callback_data="connect")],
        [InlineKeyboardButton(text="🛒 Магазин",callback_data="shop")],
        [InlineKeyboardButton(text="🎟 Активировать промокод",callback_data="promo")],
        [InlineKeyboardButton(text="🎁 Реферальная программа",callback_data="ref")],
        [InlineKeyboardButton(text="ℹ️ О сервисе",callback_data="about")],
    ])

def plans():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц — 118 ₽",callback_data="plan:1m")],
        [InlineKeyboardButton(text="3 месяца — 318 ₽",callback_data="plan:3m")],
        [InlineKeyboardButton(text="6 месяцев — 618 ₽",callback_data="plan:6m")],
        [InlineKeyboardButton(text="1 год — 1418 ₽",callback_data="plan:12m")],
        [InlineKeyboardButton(text="⬅️ Назад",callback_data="home")],
    ])

def back():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад",callback_data="home")]])

def pay(plan):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Telegram Stars",callback_data=f"pay:stars:{plan}")],
        [InlineKeyboardButton(text="🪙 CryptoBot",callback_data=f"pay:crypto:{plan}")],
        [InlineKeyboardButton(text="💳 Platega",callback_data=f"pay:platega:{plan}")],
        [InlineKeyboardButton(text="⬅️ Назад",callback_data="shop")],
    ])
