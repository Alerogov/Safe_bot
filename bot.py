from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = '7818144959:AAESBS3xLu4935xPt5Z3GZIKBiUnwO9AbJc'

# Оновлений список питань
QUESTIONS = [
  {"question": "У лісі лежить дивний предмет із дротами. Що робити?", "correct": "Не чіпай, повідом дорослих або 101", "wrong": "Розглянь ближче, можливо, це щось корисне"},
  {"question": "Друг знайшов стару гранату. Що робити?", "correct": "Зупини друга, відійдіть і подзвоніть 101", "wrong": "Спробуй розібрати її"},
  {"question": "Ти почув незрозумілий звук у землі. Що робити?", "correct": "Зупинись і поклич дорослого", "wrong": "Спробуй копати"},
  {"question": "Бачиш табличку з черепом і написом 'Міни'. Що робити?", "correct": "Обійди цю місцевість якомога далі", "wrong": "Сфотографуй її зблизька"},
  {"question": "На дорозі лежить дивна коробка. Що робити?", "correct": "Не підходь і скажи дорослим або зателефонуй 101", "wrong": "Відкрий і подивись, що всередині"},
  {"question": "Під час прогулянки знайшов снаряд. Що робити?", "correct": "Негайно відійти і попередити інших", "wrong": "Покрути його, щоб зрозуміти, що це"},
  {"question": "Друг приніс підозрілий предмет додому. Твої дії?", "correct": "Скажи дорослим і тримайся подалі", "wrong": "Пограйтесь ним, поки ніхто не бачить"},
  {"question": "На вулиці виявили невідомий рюкзак. Що робити?", "correct": "Повідомити дорослим або поліції", "wrong": "Відкрити і перевірити, чи є щось цікаве"},
  {"question": "У школі знайшли невідомий предмет. Твої дії?", "correct": "Попередити вчителя і не чіпати", "wrong": "Сховати його, щоб ніхто не знайшов"},
  {"question": "У тебе вдома залишилась невідома річ після гостей. Що робити?", "correct": "Скажи батькам і не торкайся", "wrong": "Роздивися сам і включи, якщо є кнопки"},
  {"question": "Під час пікніка хтось викопав дивну залізну річ. Що робити?", "correct": "Негайно зупинити і відійти", "wrong": "Дістати повністю, раптом це скарб"},
  {"question": "Знайшов у землі металевий предмет. Що робити?", "correct": "Відійди та попередь інших", "wrong": "Витягни і подивись"},
  {"question": "Тобі показали дивну штуку, схожу на вибухівку. Що робити?", "correct": "Скажи дорослим або подзвони 101", "wrong": "Передай іншому другу, щоб подивився"},
  {"question": "У лісі на гілці висить дріт. Твої дії?", "correct": "Обійди і повідом дорослих", "wrong": "Доторкнись, раптом це пастка для тварин"},
  {"question": "На полі стоїть табличка 'Небезпека'. Що робити?", "correct": "Обійди і не заходь на поле", "wrong": "Зайди туди, бо цікаво"},
  {"question": "Почув гучний вибух неподалік. Що робити?", "correct": "Сховайся в безпечному місці та повідом дорослих", "wrong": "Біжи ближче подивитись"},
  {"question": "У знайомого є снаряд як 'сувенір'. Що робити?", "correct": "Скажи дорослим, це небезпечно", "wrong": "Доторкнись і сфотографуй"},
  {"question": "Бачиш, як незнайомий дорослий копає в забороненій зоні. Твої дії?", "correct": "Не підходь і повідом поліцію", "wrong": "Підійди і запитай, що він шукає"},
  {"question": "Почув клацання під ногою в полі. Що робити?", "correct": "Завмерти і кликати на допомогу", "wrong": "Підніми ногу і біжи"},
  {"question": "Під час гри на подвір’ї знайшли шматок металу. Що робити?", "correct": "Не чіпати і сказати батькам", "wrong": "Кинути, як м’яч"},
  {"question": "Після дощу з-під землі виглядає щось дивне. Що робити?", "correct": "Не торкайся і попередь дорослих", "wrong": "Витягни і подивись"},
  {"question": "У парку бачиш прив’язану коробку до дерева. Що робити?", "correct": "Повідом охорону або поліцію", "wrong": "Відв’яжи і заглянь"},
  {"question": "Побачив, як діти кидають щось схоже на вибухівку. Твої дії?", "correct": "Зупини їх і поклич дорослого", "wrong": "Приєднайся до гри"},
  {"question": "Хтось пропонує купити 'стару гранату'. Що робити?", "correct": "Негайно сказати поліції", "wrong": "Візьми, якщо дешево"},
  {"question": "У школі хтось хвалиться вибухонебезпечним предметом. Твої дії?", "correct": "Повідом учителя або поліцію", "wrong": "Розпитай, де взяв"},
  {"question": "На пляжі знайшов дивну бляшанку з дротами. Що робити?", "correct": "Не чіпай і повідом 101", "wrong": "Візьми додому"},
  {"question": "Під деревом бачиш предмет з антенами. Що робити?", "correct": "Утримайся від дій і поклич дорослого", "wrong": "Подивись, чи працює"},
  {"question": "Бачиш, як хтось розкопує снаряд. Твої дії?", "correct": "Не підходь і виклич поліцію", "wrong": "Підійди і допоможи"},
  {"question": "Друг пропонує сховати знайдений снаряд. Твої дії?", "correct": "Відмов і повідом дорослих", "wrong": "Допоможи сховати"},
  {"question": "На стежці — тріснута металева банка. Що робити?", "correct": "Не чіпай — це може бути вибухівка", "wrong": "Розчави ногою"},
  {"question": "У знайомих вдома побачив міну. Що робити?", "correct": "Скажи дорослим або зателефонуй 101", "wrong": "Доторкнись і сфотографуй"},
  {"question": "На пляжі натрапив на щось, схоже на міну. Що робити?", "correct": "Негайно відійти та попередити інших", "wrong": "Копни ногою"},
  {"question": "У полі знайшли круглий предмет з отвором. Що робити?", "correct": "Не торкатися й сказати дорослим", "wrong": "Кинь у нього камінь"},
  {"question": "Хтось розповідає, що тримає міни в сараї. Твої дії?", "correct": "Скажи дорослим або поліції", "wrong": "Запитай, чи можна подивитися"},
  {"question": "На прогулянці знайшов старий патрон. Що робити?", "correct": "Не чіпай і скажи дорослим", "wrong": "Пограйся ним"},
  {"question": "Друг грає з підозрілим предметом. Що робити?", "correct": "Зупини і повідом дорослих", "wrong": "Пограйся разом"},
  {"question": "Побачив, як хтось кидає щось у вогонь. Що робити?", "correct": "Негайно відійти і попередити дорослих", "wrong": "Почекай, що буде"},
  {"question": "У лісі натрапив на металевий круг. Що робити?", "correct": "Не чіпай і повідом 101", "wrong": "Наступи, щоб перевірити"},
  {"question": "Біля школи хтось залишив коробку. Твої дії?", "correct": "Повідом учителя або поліцію", "wrong": "Відкрий подивитись, що там"}
]


user_data = {}

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶️ Почати гру", callback_data="start_game")],
        [InlineKeyboardButton("ℹ️ Про гру", callback_data="about")],
        [InlineKeyboardButton("📋 Правила безпеки", callback_data="rules")]
    ]
    await update.message.reply_text("🏁 Обери дію:", reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "about":
        keyboard = [[InlineKeyboardButton("🏠 Головне меню", callback_data="menu")]]
        await query.edit_message_text("Цей бот допомагає дітям навчитися розпізнавати вибухонебезпечні предмети через гру.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if query.data == "rules":
        keyboard = [[InlineKeyboardButton("🏠 Головне меню", callback_data="menu")]]
        await query.edit_message_text("📌 Правила:\n1. Не чіпай підозрілі предмети.\n2. Повідом дорослих або подзвони 101.\n3. Грай уважно та безпечно!", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if query.data == "menu":
        await query.message.edit_text("🏠 Повернення до головного меню.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Почати гру", callback_data="start_game")],
            [InlineKeyboardButton("ℹ️ Про гру", callback_data="about")],
            [InlineKeyboardButton("📋 Правила безпеки", callback_data="rules")]
        ]))
        return

    if query.data == "start_game":
        questions = random.sample(QUESTIONS, len(QUESTIONS))
        user_data[user_id] = {"questions": questions, "index": 0}
        await send_question(query, user_id)
        return

    if query.data.startswith("answer_"):
        selected = query.data.split("_")[1]
        index = user_data[user_id]["index"]
        question = user_data[user_id]["questions"][index]

        if selected == "correct":
            user_data[user_id]["index"] += 1
            if user_data[user_id]["index"] < len(user_data[user_id]["questions"]):
                await query.edit_message_text("✅ Вірно! +1 бал!")
                await send_question(query, user_id)
            else:
                await query.edit_message_text("🏆 Вітаємо! Ви пройшли всі рівні!")
        else:
            keyboard = [[InlineKeyboardButton("🔁 Повторити рівень", callback_data="retry")]]
            await query.edit_message_text("❌ Неправильно! Спробуй ще раз.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if query.data == "retry":
        await send_question(query, user_id, retry=True)

async def send_question(query, user_id, retry=False):
    index = user_data[user_id]["index"]
    question = user_data[user_id]["questions"][index]
    keyboard = [
        [InlineKeyboardButton(question["correct"], callback_data="answer_correct")],
        [InlineKeyboardButton(question["wrong"], callback_data="answer_wrong")]
    ]
    if retry:
        await query.edit_message_text(f"🔁 Завдання {index+1}:\n{question['question']}", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.message.reply_text(f"🧩 Завдання {index+1}:\n{question['question']}", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот працює...")
    app.run_polling()