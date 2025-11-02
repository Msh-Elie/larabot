import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

# --- CONFIG LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.info("Démarrage du bot...")

# === CONFIGURATION ===
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CANAL_ID = int(os.environ.get("CANAL_ID", 0))
CANAL_LINK = os.environ.get("CANAL_LINK")
IMAGE_PATH = os.environ.get("IMAGE_PATH", "assets/pu.jpg")

# Vérifie que l'image existe
if not os.path.exists(IMAGE_PATH):
    logging.warning(f"⚠ Image introuvable : {os.path.abspath(IMAGE_PATH)}")
else:
    logging.info(f"✅ Image trouvée : {os.path.abspath(IMAGE_PATH)}")

# === VARIABLES ===
users_confirmed = {}

# === MESSAGE D’ACCUEIL ===
WELCOME_MESSAGE = (
"Bienvenue sur le canal de Cindy Lopes \n"
    "C'est ici que l'on va pouvoir faire connaissance !\n\n"
    "Avant d'accéder à mon canal privé 🔞\n\n"
    "Est-ce que tu es bien majeur ? 😏"
)

# --- Fonction réutilisable pour envoyer le welcome ---
async def send_welcome(user_id, bot):
    keyboard = [[InlineKeyboardButton("✅ OUI, JE SUIS MAJEUR", callback_data="oui")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        with open(IMAGE_PATH, "rb") as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=WELCOME_MESSAGE,
                reply_markup=reply_markup
            )
            logging.info(f"✅ Message de bienvenue envoyé à {user_id}")
    except Exception as e:
        logging.error(f"Erreur envoi photo/bouton à {user_id}: {e}")

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome(update.effective_user.id, context.bot)

# --- Bouton ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    logging.info(f"Bouton pressé par {user_id}, data={query.data}")

    if query.data == "oui":
        users_confirmed[user_id] = True
        keyboard = [[InlineKeyboardButton("👉 Accéder au canal privé 💋", url=CANAL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.message.reply_text(
                "En attendant, tu peux me follow sur insta 😌\n\n"
                "👉 https://www.instagram.com/cindylopesoff?igsh=eGw5MXZ2ZjNyNWc5\n\n"
                "À tout de suite ❤\n\nClique ci-dessous pour rejoindre le canal 💋",
                reply_markup=reply_markup
            )
            logging.info("Message avec lien canal envoyé.")
        except Exception as e:
            logging.error(f"Erreur envoi message bouton : {e}")

        try:
            await context.bot.approve_chat_join_request(chat_id=CANAL_ID, user_id=user_id)
            logging.info(f"Demande d’approbation acceptée pour {user_id}")
        except Exception as e:
            logging.warning(f"Impossible d’approuver {user_id}: {e}")

# --- Demande de rejoindre le canal ---
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    logging.info(f"Requête join reçue de {user_id} → on envoie le welcome")
    await send_welcome(user_id, context.bot)

# === CONFIGURATION DU BOT ===
app_bot = ApplicationBuilder().token(TOKEN).build()

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(button))
app_bot.add_handler(ChatJoinRequestHandler(on_join_request))

# === LANCEMENT DU BOT (polling) ===
if __name__ == "__main__":
    logging.info("🚀 Lancement du bot en mode POLLING (Render Background Worker)")
    app_bot.run_polling(drop_pending_updates=True)

