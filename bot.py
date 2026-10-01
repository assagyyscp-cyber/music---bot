import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from dotenv import load_dotenv


# =========================
# НАСТРОЙКИ
# =========================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@vukoul"

# Ссылка на нашу Telegram Mini App
WEB_APP_URL = "https://assagyyscp-cyber.github.io/music---bot/"


# =========================
# ПРОВЕРКА ТОКЕНА
# =========================

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN не найден. Добавь BOT_TOKEN в Variables на Railway."
    )


# =========================
# BOT / DISPATCHER
# =========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# КЛАВИАТУРА ПОДПИСКИ
# =========================

def subscription_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Подписаться на канал",
                    url="https://t.me/vukoul"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я подписался",
                    callback_data="check_subscription"
                )
            ]
        ]
    )


# =========================
# КЛАВИАТУРА MUSIC
# =========================

def music_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎧 Открыть MUSIC",
                    web_app=WebAppInfo(
                        url=WEB_APP_URL
                    )
                )
            ]
        ]
    )


# =========================
# ПРОВЕРКА ПОДПИСКИ
# =========================

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        return member.status in {
            "member",
            "administrator",
            "creator"
        }

    except Exception as e:
        print("Ошибка проверки подписки:", e)
        return False


# =========================
# /START
# =========================

@dp.message(CommandStart())
async def start(message: types.Message):

    user_id = message.from_user.id

    # Проверяем подписку
    if not await check_subscription(user_id):

        await message.answer(
            "🎵 <b>MUSIC</b>\n\n"
            "Добро пожаловать!\n\n"
            "Чтобы пользоваться MUSIC, "
            "сначала подпишитесь на наш канал 👇",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # Если подписан
    await message.answer(
        "🎵 <b>MUSIC</b>\n\n"
        "✅ Подписка подтверждена!\n\n"
        "Добро пожаловать в MUSIC 🎧",
        reply_markup=music_keyboard(),
        parse_mode="HTML"
    )


# =========================
# КНОПКА «Я ПОДПИСАЛСЯ»
# =========================

@dp.callback_query(
    lambda callback: callback.data == "check_subscription"
)
async def check_subscription_button(
    callback: types.CallbackQuery
):

    user_id = callback.from_user.id

    # Проверяем подписку заново
    if not await check_subscription(user_id):

        await callback.answer(
            "❌ Вы ещё не подписались на канал",
            show_alert=True
        )

        return

    # Подписка подтверждена
    await callback.message.edit_text(
        "🎵 <b>MUSIC</b>\n\n"
        "✅ Подписка подтверждена!\n\n"
        "Теперь можно открыть музыкальное приложение 🎧",
        reply_markup=music_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer("✅ Готово!")


# =========================
# ЗАПУСК
# =========================

async def main():

    print("🎵 MUSIC BOT запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
