import asyncio
import aioredis
import os

from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
redis = aioredis.from_url("redis://localhost")


async def send_message(chat_id: int, text: str) -> None:
    bot = Bot(BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)


async def send_message_to_all(text: str) -> None:
    for chat_id in {
        await redis.lindex("chats", index)
        for index in range(0, await redis.llen("chats"))
    }:
        await send_message(chat_id=int(chat_id), text=text)


if __name__ == "__main__":
    # chat_id = int(input("Enter chat ID: "))
    # text = input("Your message: ")
    # asyncio.run(send_message(chat_id=chat_id, text=text))

    text = input("Your message: ")
    asyncio.run(send_message_to_all(text=text))

