import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# ----- НАСТРОЙКИ -----
# Вставьте токен, который дал @BotFather (в кавычках)
BOT_TOKEN = "8855742069:AAETXoEElDRsf3AvZhUOk2h5nBkQSrP8Yjw" 
# Вставьте ваш личный ID от @userinfobot (БЕЗ кавычек)
ADMIN_ID = 7653361533
# ---------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Приветствие для клиента (когда нажал Старт на сайте)
@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer(
        "👋 Здравствуйте! Вы обратились в службу поддержки.\n\n"
        "Напишите ваш вопрос прямо сюда, и наш менеджер ответит вам в ближайшее время!"
    )

# Пересылка сообщения от клиента — АДМИНУ
@dp.message(F.chat.type == "private")
async def forward_to_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        # Пересылаем сообщение админу (так сохранится связь для ответа)
        forwarded = await message.forward(chat_id=ADMIN_ID)
        
        # Дополнительно отправляем текст с ID, чтобы вы знали, кто пишет
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 **Новый вопрос!**\n"
                 f"От: {message.from_user.full_name} (@{message.from_user.username})\n"
                 f"ID: `{message.from_user.id}`\n"
                 f"☝️ Используйте функцию 'Ответить' (Reply) на ПЕРЕСЛАННОЕ сообщение выше, чтобы написать клиенту.",
            parse_mode="Markdown",
            reply_to_message_id=forwarded.message_id
        )
    else:
        # Если админ отвечает на ПЕРЕСЛАННОЕ сообщение клиента
        if message.reply_to_message and message.reply_to_message.forward_from:
            client_id = message.reply_to_message.forward_from.id
            try:
                # Отправляем ответ клиенту
                await bot.send_message(chat_id=client_id, text=f"💬 **Ответ поддержки:**\n\n{message.text}")
                await message.answer("✅ Ответ успешно отправлен клиенту!")
            except Exception as e:
                await message.answer(f"❌ Не удалось отправить ответ. Возможно, пользователь заблокировал бота. Ошибка: {e}")
        else:
            await message.answer("Чтобы ответить клиенту, сделайте 'Reply' (Ответить) на его пересланное сообщение.")

async def main():
    print("🤖 Бот поддержки успешно запущен внутри VS Code!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    