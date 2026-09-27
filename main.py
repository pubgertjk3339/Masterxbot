import os
import telebot
from flask import Flask, request

# Гирифтани Токени бот аз Render Environment
TOKEN = os.environ.get("8953447600:AAFQ122JJY2WMNUQIGQuaFUZ8E3NwXFT4f4")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ID-ҲОИ АДМИНҲО (Шумо ва Дӯстат) ---
ADMIN_IDS = [
    7811559530,  # <-- ID-и рақамии худро ин ҷо гузоред
    8289634462,  # <-- ID-и рақамии дӯстатро ин ҷо гузоред
]

# Рӯйхати канали пайвастшуда (Танҳо як ё чанд канал метавонад бошад)
CONNECTED_CHANNELS = []

# Базаи калимаҳои калидӣ барои ҷустуҷӯ ва пайваст кардани онҳо ба паёмҳои канал
# (Формат: "калимаи ҷустуҷӯӣ": "Матни пурраи паём ё маълумоти маҳсулот")
SEARCH_DATABASE = {
    "pubg": (
        "🎮 *PUBG Mobile Account (Ледник)*\n"
        "🔸 Видеоаш: Дорад (дар канал)\n"
        "🔸 ЛЕДНИК: Дараҷаи лозима\n"
        "🔸 Нарх: 300 сомонӣ\n"
        "👉 Барои харид ба админ нависед!"
    ),
    "free fire": (
        "🔥 *Free Fire Account*\n"
        "🔸 Элит Пасс ва скинҳои зӯр\n"
        "🔸 Нарх: 150 сомонӣ"
    ),
}


# --- ФАРМОНИ ОСАСӢ (/start) ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
  markup = telebot.types.ReplyKeyboardMarkup(
      resize_keyboard=True, row_width=2
  )
  btn_search = telebot.types.KeyboardButton("🔍 Ҷустуҷӯи Маҳсулот")
  btn_list = telebot.types.KeyboardButton("📋 Рӯйхати Ҳамааш")
  btn_info = telebot.types.KeyboardButton("ℹ️ Маълумот")

  if message.from_user.id in ADMIN_IDS:
    btn_admin = telebot.types.KeyboardButton("⚙️ Панели Админ")
    markup.add(btn_search, btn_list, btn_admin, btn_info)
  else:
    markup.add(btn_search, btn_list, btn_info)

  welcome_text = (
      f"Салом, *{message.from_user.first_name}*!\n\n"
      "Хуш омадед ба платформаи мо.\n"
      "Барои ёфтани маҳсулот ё акаунт, метавонед тугмаи ҷустуҷӯро пахш кунед ё номи онро нависед!"
  )
  bot.send_message(
      message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup
  )


# --- КОРКАРДИ ПАЁМҲО ВА ФУНКСИЯҲО ---
@bot.message_handler(func=lambda message: True)
def handle_user_messages(message):
  text = message.text.strip()
  user_id = message.from_user.id

  if text == "🔍 Ҷустуҷӯи Маҳсулот":
    bot.send_message(
        message.chat.id,
        "✍️ Лутфан номи чизе ки мехоҳед нависед (ҳатто бо 2 ҳарф, масалан: `pu` ё `free`):",
        parse_mode="Markdown",
    )
    return

  elif text == "📋 Рӯйхати Ҳамааш":
    response_list = "📋 **Маҳсулоти мавҷуда:**\n\n"
    for key in SEARCH_DATABASE.keys():
      response_list += f"• `{key.title()}`\n"
    bot.send_message(message.chat.id, response_list, parse_mode="Markdown")
    return

  elif text == "ℹ️ Маълумот":
    bot.send_message(
        message.chat.id,
        "💎 Ин бот барои ба таври худкор пайдо кардани эълонҳои канал сохта шудааст.",
        parse_mode="Markdown",
    )
    return

  elif text == "⚙️ Панели Админ":
    if user_id in ADMIN_IDS:
      channels_str = (
          "\n".join(CONNECTED_CHANNELS)
          if CONNECTED_CHANNELS
          else "Ҳоло ягон канал пайваст нест."
      )
      bot.send_message(
          message.chat.id,
          "⚙️ **Панели идоракунии Админҳо:**\n\n"
          "📌 **Канали шумо:**\n"
          f"{channels_str}\n\n"
          "➕ **Танҳо бо 1 фармон каналро ҳамроҳ кунед:**\n"
          "`/addchannel | @nika_kanal`\n\n"
          "➕ **Илова кардани маълумот (масалан леднк 300 сомонӣ):**\n"
          "`/add | калимаи ҷустуҷӯ | матни пурраи эълон аз канал`",
          parse_mode="Markdown",
      )
    else:
      bot.send_message(message.chat.id, "❌ Шумо ҳуқуқи админӣ надоред.")
    return

  # --- ФАРМОНИ АДМИН: Илова кардани канал танҳо бо 1 ник ---
  if text.startswith("/addchannel"):
    if user_id in ADMIN_IDS:
      try:
        parts = text.split("|")
        if len(parts) >= 2:
          channel_nik = parts[1].strip()
          if channel_nik not in CONNECTED_CHANNELS:
            CONNECTED_CHANNELS.append(channel_nik)
            bot.send_message(
                message.chat.id,
                f"✅ Канали `{channel_nik}` бомуваффақият илова шуд! Акнун бот ба он пайваст аст.",
                parse_mode="Markdown",
            )
          else:
            bot.send_message(
                message.chat.id, "⚠️ Ин канал аллакай дар рӯйхат ҳаст."
            )
        else:
          bot.send_message(
              message.chat.id,
              "⚠️ Формати нодуруст! Истифода баред:\n`/addchannel | @nika_kanal`",
              parse_mode="Markdown",
          )
      except Exception as e:
        bot.send_message(message.chat.id, f"❌ Хатогӣ: {e}")
    else:
      bot.send_message(message.chat.id, "❌ Танҳо админҳо метавонанд ин корро кунанд.")
    return

  # --- ФАРМОНИ АДМИН: Илова кардани матни пурра (масалан леднк 300 сомони) ---
  if text.startswith("/add") and not text.startswith("/addchannel"):
    if user_id in ADMIN_IDS:
      try:
        parts = text.split("|")
        if len(parts) >= 3:
          keyword = parts[1].strip().lower()
          full_content = parts[2].strip()
          SEARCH_DATABASE[keyword] = full_content
          bot.send_message(
              message.chat.id,
              f"✅ Маълумот бо калимаи `'{keyword}'` илова шуд!",
              parse_mode="Markdown",
          )
        else:
          bot.send_message(
              message.chat.id,
              "⚠️ Формати нодуруст!\nИстифода баред:\n`/add | калима | матни пурраи эълон бо нарху видео`",
              parse_mode="Markdown",
          )
      except Exception as e:
        bot.send_message(message.chat.id, f"❌ Хатогӣ: {e}")
    else:
      bot.send_message(message.chat.id, "❌ Танҳо админҳо метавонанд ин корро кунанд.")
    return

  # --- АЛГОРИТМИ ҶУСТӮҶӮИ ЧАНДИР БАРОИ КОРБАРОН (Ҳатто бо 2 ҳарф) ---
  query = text.lower()
  found_results = []

  for key, details in SEARCH_DATABASE.items():
    # Агар корбар ҳатто 2 ҳарфи онро нависад (масалан "pu" ё "le") меёбад
    if query in key or query in details.lower():
      found_results.append(details)

  if found_results:
    bot.send_message(
        message.chat.id, "🔍 **Эълон ва маълумоти ёфтшуда:**", parse_mode="Markdown"
    )
    for result in found_results:
      bot.send_message(message.chat.id, result, parse_mode="Markdown")
  else:
    bot.send_message(
        message.chat.id,
        f"❌ Аз рӯи дархости `'{text}'` ягон маълумот ёфт нашуд.\n"
        "Лутфан номи дурусти онро нависед.",
        parse_mode="Markdown",
    )


# --- СЕРВЕРИ FLASK ВА ВЕБҲУК БАРОИ RENDER ---
@app.route("/")
def index():
  return "MASTER X Channel Bot is running 24/7!", 200


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
  if request.headers.get("content-type") == "application/json":
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
  else:
    return "Invalid request", 403


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))

  RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
  if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

  app.run(host="0.0.0.0", port=port)
