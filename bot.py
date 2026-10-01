import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@vukoul"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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


def music_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎧 Открыть MUSIC",
                    callback_data="open_music"
                )
            ]
        ]
    )


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
        print("Ошибка проверки:", e)
        return False


@dp.message(CommandStart())
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "🎵 <b>MUSIC</b>\n\n"
            "Добро пожаловать!\n\n"
            "Чтобы пользоваться ботом, "
            "сначала подпишитесь на наш канал 👇",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )
        return

    await message.answer(
        "🎵 <b>MUSIC</b>\n\n"
        "✅ Подписка подтверждена!\n\n"
        "Добро пожаловать в MUSIC 🎧",
        reply_markup=music_keyboard(),
        parse_mode="HTML"
    )


@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription_button(
    callback: types.CallbackQuery
):
    if not await check_subscription(callback.from_user.id):
        await callback.answer(
            "❌ Вы ещё не подписались",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "🎵 <b>MUSIC</b>\n\n"
        "✅ Подписка подтверждена!\n\n"
        "Добро пожаловать в MUSIC 🎧",
        reply_markup=music_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer("✅ Готово!")


@dp.callback_query(lambda c: c.data == "open_music")
async def open_music(callback: types.CallbackQuery):
    await callback.answer(
        "🎧 Скоро здесь будет MUSIC!"
    )


async def main():
    print("🎵 MUSIC BOT запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
