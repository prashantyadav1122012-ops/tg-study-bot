from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq
import os

BOT_TOKEN = "8903195952:AAEJoKA10DIkTynMzPNVGpixgGukjuFmsEg"
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

WELCOME = """👋 Welcome to Study AI Bot!

📚 Main aapka AI Study Assistant hoon.

✅ Kisi bhi study question ka answer dunga.
✅ Hindi aur English dono me explain karunga.
✅ Step-by-step solution dunga.

✍️ Ab apna question bhejiye."""

SYSTEM = (
    "You are a helpful study assistant. Answer only educational questions. "
    "If the user asks something unrelated to studies, politely refuse. "
    "Explain in simple Hindi + English."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":q}
        ]
    )
    await update.message.reply_text(resp.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot is running...")
app.run_polling()
