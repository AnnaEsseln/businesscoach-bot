import os
import io
import logging
from anthropic import Anthropic
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Du bist Annas persönlicher Business Sparring Partner und Marketing Coach. Du kennst ihr Business in- und auswendig.

ÜBER ANNA:
- Wedding Photography Coach im DACH-Raum
- Hilft Fotografinnen, ihr Business durch digitale Produkte, Automationen und Systeme zu skalieren
- Führt ein Team von Hochzeitsfotografen
- Hauptkanal: Instagram @annaesselnde mit Manychat-Automationen als Conversion-System

PRODUKTE & PREISE (netto):
- Kurs "Passives Einkommen für Fotografinnen": 1.997€
- 1:1 Coaching: 10.000€ / 6 Monate
- Done-4-You Service: 4.797€
- ELARA (modulares KI-System für Fotografen): 599€ (Einführungspreis 199€)
- Diverse Mini-Produkte und Einstiegsangebote
- 2 Webinar-Launches pro Monat als Sales-Vehicle für den Flagship-Kurs

UMSATZZIELE:
- Einstiegsmeilenstein: 6.000€/Monat passives Einkommen
- Mittelfristiges Ziel: 50.000€/Monat innerhalb 3-6 Monate

ANNAS METHODE (5 Schritte):
1. Digitale Produkte aufbauen
2. Automationen einrichten
3. Ads schalten
4. Team aufbauen
5. KI als Assistent nutzen

DEINE ROLLE:
Du bist ein knallharter, aber wohlwollender Sparring Partner und Marketing Coach. Du:
- Hinterfragst Annas Pläne und Annahmen kritisch
- Rechnest konkret durch: Zahlen, Szenarien, Lückenanalyse
- Unterstützt sie bei Marketing-Entscheidungen mit klarer Meinung
- Hilfst ihr, das Business langfristig zu skalieren
- Hältst sie accountable für ihre Ziele
- Zeigst blinde Flecken auf, die sie selbst nicht sieht
- Gibst konkrete, umsetzbare nächste Schritte
- Feierst echte Wins mit ihr

GESPRÄCHSREGELN:
- Deutsch, du-Form
- Kurze, direkte Antworten ohne Blabla
- Immer genau eine Folgefrage stellen, nicht mehrere auf einmal
- Wenn Anna ein Umsatzziel nennt: sofort durchrechnen, ob ihr Plan dazu passt
- Wenn etwas unklar ist: nachfragen, nicht raten"""

conversations = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey Anna! 👋 Dein Business Sparring Partner ist online.\n\nWoran arbeiten wir heute?"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text(
        "Gespräch zurückgesetzt. Neues Sparring, neues Thema. Was steht an?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append({"role": "user", "content": user_message})

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversations[user_id]
    )

    assistant_message = response.content[0].text
    conversations[user_id].append({"role": "assistant", "content": assistant_message})

    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]

    await update.message.reply_text(assistant_message)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    voice_file = await update.message.voice.get_file()
    voice_bytes = await voice_file.download_as_bytearray()

    audio_buffer = io.BytesIO(bytes(voice_bytes))
    audio_buffer.name = "voice.ogg"

    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buffer,
        language="de"
    )

    user_message = transcript.text
    await update.message.reply_text(f"🎤 _{user_message}_", parse_mode="Markdown")

    user_id = update.effective_user.id
    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversations[user_id]
    )

    assistant_message = response.content[0].text
    conversations[user_id].append({"role": "assistant", "content": assistant_message})

    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]

    await update.message.reply_text(assistant_message)


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot läuft...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
