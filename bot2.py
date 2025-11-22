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
logging.info("🚀 Démarrage du bot 3...")

# === CONFIGURATION ===
TOKEN2 = os.environ.get("TELEGRAM_TOKEN2")
CANAL_ID2 = int(os.environ.get("CANAL_ID2", 0))
CANAL_LINK2 = os.environ.get("CANAL_LINK2")
IMAGE_PATH2 = os.environ.get("IMAGE_PATH2", "assets/lara.jpg")
LINK = "https://onlyfans.com/itslaramoore"
CANAL3 ="https://t.me/+x7w3ARZ7D89mNzRk"
BOT_USERNAME = "LaraCheckBot"  # Nom de ton bot

if not TOKEN2:
    logging.error("❌ TOKEN manquant ! Vérifie TELEGRAM_TOKEN2 dans les variables Render.")
    exit(1)

if not os.path.exists(IMAGE_PATH2):
    logging.warning(f"⚠ Image introuvable : {os.path.abspath(IMAGE_PATH2)}")
else:
    logging.info(f"✅ Image trouvée : {os.path.abspath(IMAGE_PATH2)}")

# === VARIABLES ===
users_confirmed = {}

# === MESSAGE D'ACCUEIL ===
WELCOME_MESSAGE = (
    "Bienvenue sur le canal de Lara 💋\n"
    "C'est ici que l'on va pouvoir faire connaissance !\n\n"
    "Avant d'accéder à mon canal privé 🔞\n\n"
    "Follow mon insta pour que je t'accepte rapidement 😘\nhttps://www.instagram.com/itslaramxre"
    "Est-ce que tu es bien majeur ? 😏"
)

# --- Fonction pour afficher le message principal après validation ---
async def show_main_menu(user_id, bot):
    """Montre le message principal et les liens après confirmation"""
    try:
        keyboard = [
        [InlineKeyboardButton("👉 Accéder au canal privé 💋", url=CANAL_LINK2)],
        [InlineKeyboardButton("Mon côté 🌶", url=LINK)]
        ]

        await bot.send_message(
            chat_id=user_id,
            text=(
                "À tout de suite ❤\n\nClique ci-dessous pour rejoindre le canal 💋"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        logging.info(f"✅ Message principal envoyé à {user_id}")
    except Exception as e:
        logging.error(f"❌ Erreur envoi message principal à {user_id}: {e}")

# --- Fonction d'envoi du premier message (welcome) ---
async def send_welcome(user_id, bot):
    # Bouton qui ouvre directement le bot avec start
    keyboard = [[InlineKeyboardButton(
        "✅ OUI, JE SUIS MAJEUR",
        url=f"https://t.me/{BOT_USERNAME}?start=confirm"
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        with open(IMAGE_PATH2, "rb") as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=WELCOME_MESSAGE,
                reply_markup=reply_markup
            )
            logging.info(f"✅ Message de bienvenue envoyé à {user_id}")
    except Exception as e:
        logging.error(f"❌ Erreur envoi photo/bouton à {user_id}: {e}")

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"/start reçu de {user_id}")

    # Vérifie si le paramètre start=confirm a été passé
    if update.message.text and "confirm" in update.message.text:
        users_confirmed[user_id] = True
        await show_main_menu(user_id, context.bot)
        try:
            await context.bot.approve_chat_join_request(chat_id=CANAL_ID2, user_id=user_id)
            logging.info(f"✅ Demande d'approbation acceptée pour {user_id}")
        except Exception as e:
            logging.warning(f"⚠ Impossible d'approuver {user_id}: {e}")
    else:
        await send_welcome(user_id, context.bot)

# --- Bouton (au cas où tu veux conserver d'autres callback) ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    logging.info(f"🟡 Bouton pressé par {user_id}, data={query.data}")

    if query.data == "oui":
        users_confirmed[user_id] = True
        await show_main_menu(user_id, context.bot)
        try:
            await context.bot.approve_chat_join_request(chat_id=CANAL_ID2, user_id=user_id)
            logging.info(f"✅ Demande d'approbation acceptée pour {user_id}")
        except Exception as e:
            logging.warning(f"⚠ Impossible d'approuver {user_id}: {e}")

# --- Demande de rejoindre le canal ---
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    logging.info(f"📨 Requête join reçue de {user_id}")
    await send_welcome(user_id, context.bot)

# === CONFIGURATION DU BOT ===
app_bot = ApplicationBuilder().token(TOKEN2).build()

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(button))
app_bot.add_handler(ChatJoinRequestHandler(on_join_request))

# === LANCEMENT DU BOT (polling) ===
if __name__ == "__main__":
    logging.info("🚀 Lancement du bot2 en mode POLLING (Render Background Worker)")
    app_bot.run_polling(drop_pending_updates=True)




