import aioredis

redis = aioredis.from_url("redis://localhost")


async def get_chat_ids() -> set:
    return {
        await redis.lindex("chats", index)
        for index in range(0, await redis.llen("chats"))
    }


async def delete_chat_ids(chat_id):
    await redis.lrem("chats", count=0, value=chat_id)
