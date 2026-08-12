import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from playwright.async_api import async_playwright

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

VOICE_URL = "https://voicelime.com/voice-generator"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "سلام علی 👋\n\n"
        "🇳🇱 ربات Voice هلندی آماده است.\n\n"
        "برای تست یک متن هلندی بفرست."
    )


async def receive_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.strip()

    await update.message.reply_text(
        "🔎 در حال بررسی Voiceهای هلندی VoiceLime..."
    )

    try:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            await page.goto(
                VOICE_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # قبول کوکی
            accept = page.get_by_role(
                "button",
                name="Accept All"
            )

            if await accept.count() > 0:

                try:
                    await accept.click(
                        timeout=3000
                    )
                except Exception:
                    pass

            # انتخاب Dutch Netherlands
            language = page.locator(
                "#languageSelect"
            )

            await language.select_option(
                "nl-NL"
            )

            # صبر برای بارگذاری Voiceها
            await page.wait_for_timeout(3000)

            # پیدا کردن Voice Select
            voice_select = page.locator(
                "#voiceSelect"
            )

            count = await voice_select.locator(
                "option"
            ).count()

            message = (
                "🇳🇱 Voiceهای Dutch (Netherlands):\n\n"
                f"تعداد Voiceها: {count}\n\n"
            )

            options = await voice_select.locator(
                "option"
            ).evaluate_all(
                """
                els => els.map(e => ({
                    text: (e.textContent || '').trim(),
                    value: e.value || ''
                }))
                """
            )

            for option in options:

                message += (
                    f"• {option['text']}\n"
                    f"  value={option['value']}\n\n"
                )

            if len(message) > 3900:

                message = (
                    message[:3900]
                    + "\n\n⚠️ ادامه لیست زیاد بود."
                )

            await update.message.reply_text(
                message
            )

            await browser.close()

    except Exception as e:

        await update.message.reply_text(
            "❌ خطا:\n\n"
            + str(e)[:1500]
        )


def main():

    app = Application.builder().token(
        TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_text
        )
    )

    print(
        "Dutch Voice Bot is running..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
