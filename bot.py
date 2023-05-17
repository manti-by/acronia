import aioredis
import os
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from utils import get_chat_ids

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis = aioredis.from_url("redis://localhost")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f"Start chat #{update.effective_chat.id} - username {update.effective_user.first_name}"
    )
    await redis.lpush("chats", update.effective_chat.id)
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}"
    )

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f"Delete chat #{update.effective_chat.id} - username {update.effective_user.first_name}"
    )
    if update.effective_chat.id not in get_chat_ids():
        await redis.lpush("chats", update.effective_chat.id)
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}"
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f"Message {update.message.text} from chat #{update.effective_chat.id}"
    )
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, message))
    app.run_polling()

