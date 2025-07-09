#!/usr/bin/env python3
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

async def test_telegram():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids_str = os.environ.get("TELEGRAM_CHAT_IDS")
    print(f"Bot token: {bot_token}")
    print(f"Chat IDs: {chat_ids_str}")
    if not bot_token or not chat_ids_str:
        print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_IDS environment variables not set.")
        return
    
    # Parse multiple chat IDs (comma-separated)
    chat_ids = [chat_id.strip() for chat_id in chat_ids_str.split(",")]
    
    try:
        bot = Bot(token=bot_token)
        for chat_id in chat_ids:
            result = await bot.send_message(
                chat_id=chat_id,
                text="🧪 *Test Message*\n\nThis is a test message from your reminder bot!",
                parse_mode=ParseMode.MARKDOWN
            )
            print(f"✅ Test message sent successfully to {chat_id}!")
            print(f"Message ID: {result.message_id}")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_telegram()) 