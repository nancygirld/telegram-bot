import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, ContextTypes

# توکن ربات — جایگزین کن با توکن واقعی خودت
BOT_TOKEN = '8105780956:AAGN5ufEN_cxJCTEmFQyrF8HRId1f48zrbQ'

# کدهای گروه‌ها
group_codes = [
    "-1001050069540",
    "1001350081541",
    "-1001150099533",
    "-1001350022560",
    "-1001750024429",
    "-1001470027110"
]

# نگهداری کد اختصاصی برای هر گروه
assigned_codes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Your user ID is {user_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "I will send you your telegram user ID, current chat ID and sender ID or chat ID of forwarded message.\n\n"
        "User ID - your unique identifier in telegram, which you can use in your telegram bot. Read more: https://core.telegram.org/bots/api#user"
    )

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id

    # اختصاص کد برای هر گروه فقط یک بار
    if chat_id not in assigned_codes:
        assigned_codes[chat_id] = random.choice(group_codes)

    group_code = assigned_codes[chat_id]

    for member in update.message.new_chat_members:
        user_id = member.id
        name = member.full_name

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"👤 Name: {name}\n"
                f"🆔 User ID: {user_id}\n"
                f"🔢 Group code: {group_code}"
            )
        )

async def forward_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.forward_from:
        await update.message.reply_text(
            f"Forward sender ID: {update.message.forward_from.id}"
        )

async def on_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    if chat_id not in assigned_codes:
        assigned_codes[chat_id] = random.choice(group_codes)
    group_code = assigned_codes[chat_id]

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"User ID: {user_id}\nGroup code: {group_code}"
    )

async def on_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Your user ID is {user_id}")

async def on_reply_to_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        if update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.is_bot:
            user_id = update.message.from_user.id
            await update.message.reply_text(f"Your user ID is {user_id}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(MessageHandler(filters.FORWARDED, forward_info))

    application.add_handler(
        MessageHandler(filters.TEXT & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP), on_group_message)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, on_private_message)
    )
    application.add_handler(
        MessageHandler(filters.REPLY, on_reply_to_bot)
    )

    application.run_polling()

if __name__ == "__main__":
    main()

