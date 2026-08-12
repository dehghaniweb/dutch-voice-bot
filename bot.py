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
