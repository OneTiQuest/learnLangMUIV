import telebot as tb
from telebot import types
from query import get_user_by_chat_id, save_user
from scripts import student_start_script, student_settings_script


TOKEN = "8271309227:AAH22j-4-MzFHekEKSFECDBtyP05_3MC0yY"
bot = tb.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        user = save_user(message.from_user)

    role = user[5]

    # Обработка ученика
    if role == 1:
        bot.send_message(
           message.chat.id,
           f"Привет, {message.from_user.first_name}👋."
        )

        student_start_script(bot, message)

    # Обработка преподавателя
    elif role == 2:
        pass

    # Обработка администратора
    elif role == 3:
        pass

# Обработчик текстовых сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = get_user_by_chat_id(message.chat.id)
    if not user:
        bot.send_message(message.chat.id, "Пользователь не найден в системе. Для регистрации напишите комманду /start")

    role = user[5]
    # Обработка ученика
    if role == 1:
        answer = student_start_script(bot, message)
        answer = student_settings_script(bot, message)
        
        if answer is None:
            bot.send_message(message.chat.id, "Я не понимаю эту команду")

    # Обработка преподавателя
    elif role == 2:
        pass

    # Обработка администратора
    elif role == 3:
        pass
    else:
        # Отправляем сообщение
        bot.send_message(
            message.chat.id,
            f"Не удалось обработать роль: {role}"
        )


# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
