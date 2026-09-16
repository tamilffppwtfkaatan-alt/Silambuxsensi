import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {}

    keyboard = [
        [
            InlineKeyboardButton("📱 Vivo", callback_data="brand_vivo"),
            InlineKeyboardButton("📱 Samsung", callback_data="brand_samsung"),
        ],
        [
            InlineKeyboardButton("📱 Redmi / Poco", callback_data="brand_redmi"),
            InlineKeyboardButton("📱 Realme", callback_data="brand_realme"),
        ],
        [
            InlineKeyboardButton("📱 Other", callback_data="brand_other"),
        ],
    ]

    await update.message.reply_text(
        "🔥 SILAMBU AUTO SENSI\n\n"
        "உங்க Mobile Brand select பண்ணுங்க 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_id not in user_data:
        user_data[user_id] = {}

    if data.startswith("brand_"):
        brand = data.replace("brand_", "")
        user_data[user_id]["brand"] = brand

        keyboard = [
            [
                InlineKeyboardButton("4 GB RAM", callback_data="ram_4"),
                InlineKeyboardButton("6 GB RAM", callback_data="ram_6"),
            ],
            [
                InlineKeyboardButton("8 GB RAM", callback_data="ram_8"),
                InlineKeyboardButton("12 GB+ RAM", callback_data="ram_12"),
            ],
        ]

        await query.edit_message_text(
            "💾 RAM select பண்ணுங்க 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data.startswith("ram_"):
        ram = data.replace("ram_", "")
        user_data[user_id]["ram"] = ram

        keyboard = [
            [
                InlineKeyboardButton("🎯 One Tap", callback_data="style_onetap"),
            ],
            [
                InlineKeyboardButton("⚡ Drag Headshot", callback_data="style_drag"),
            ],
            [
                InlineKeyboardButton("🔥 Balanced", callback_data="style_balanced"),
            ],
        ]

        await query.edit_message_text(
            "🎮 உங்க Play Style select பண்ணுங்க 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data.startswith("style_"):
        style = data.replace("style_", "")
        user_data[user_id]["style"] = style

        result = generate_sensi(user_data[user_id])

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄 Generate Again",
                    callback_data="regenerate",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Start Again",
                    callback_data="restart",
                )
            ],
        ]

        await query.edit_message_text(
            result,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data == "regenerate":
        result = generate_sensi(user_data[user_id])

        await query.edit_message_text(
            result,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 Generate Again",
                            callback_data="regenerate",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🏠 Start Again",
                            callback_data="restart",
                        )
                    ],
                ]
            ),
        )

    elif data == "restart":
        await start_from_button(query, user_id)


async def start_from_button(query, user_id):
    user_data[user_id] = {}

    keyboard = [
        [
            InlineKeyboardButton("📱 Vivo", callback_data="brand_vivo"),
            InlineKeyboardButton("📱 Samsung", callback_data="brand_samsung"),
        ],
        [
            InlineKeyboardButton("📱 Redmi / Poco", callback_data="brand_redmi"),
            InlineKeyboardButton("📱 Realme", callback_data="brand_realme"),
        ],
        [
            InlineKeyboardButton("📱 Other", callback_data="brand_other"),
        ],
    ]

    await query.edit_message_text(
        "🔥 SILAMBU AUTO SENSI\n\n"
        "உங்க Mobile Brand select பண்ணுங்க 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def generate_sensi(data):
    style = data.get("style", "balanced")

    if style == "onetap":
        general = 98
        red_dot = 94
        scope2x = 88
        scope4x = 82
        sniper = 55
        free_look = 75

    elif style == "drag":
        general = 96
        red_dot = 92
        scope2x = 86
        scope4x = 80
        sniper = 52
        free_look = 72

    else:
        general = 94
        red_dot = 90
        scope2x = 84
        scope4x = 78
        sniper = 50
        free_look = 70

    return (
        "🔥 SILAMBU AUTO SENSI\n\n"
        f"📱 Brand: {data.get('brand', 'Unknown').title()}\n"
        f"💾 RAM: {data.get('ram', '?')} GB\n"
        f"🎯 Style: {style.title()}\n\n"
        "━━━━━━━━━━━━━━\n"
        "🎮 YOUR SENSI\n"
        "━━━━━━━━━━━━━━\n\n"
        f"🔴 General     : {general}\n"
        f"🔴 Red Dot     : {red_dot}\n"
        f"🔭 2X Scope    : {scope2x}\n"
        f"🔭 4X Scope    : {scope4x}\n"
        f"🎯 Sniper      : {sniper}\n"
        f"👁️ Free Look   : {free_look}\n\n"
        "━━━━━━━━━━━━━━\n"
        "⚡ Generated by SILAMBU AUTO SENSI"
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
