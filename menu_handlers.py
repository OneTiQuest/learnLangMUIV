from check_answers import lang_answer, course_answer, role_answer, module_answer
import markups
from query import set_user_lang, upsert_settings, get_exercise, save_answer, update_role, set_user_grade, get_teacer_stat, get_users
from query import create_module, create_theme, update_module, update_theme, delete_module, delete_theme
from exersise_handlers import ExersiseFactory
from scripts import calc_result
import state

def _1_step_handler(bot, user_id: int, text: str):
    answer = lang_answer(text)
    if answer:
        set_user_lang(user_id, answer[0])
        bot.send_message(user_id, f'Текущий язык для обучения: {text}')

        state.set_state(user_id, '2_step')
        bot.send_message(
            user_id, 
            "Смена курса обучения:", 
            reply_markup=markups.get_course_markup()
        )

    else:
        bot.send_message(
            user_id, 
            "Смена языка обучения:", 
            reply_markup=markups.get_lang_markup()
        )

def _2_step_handler(bot, user_id: int, text: str):
    answer = course_answer(text)
    if answer:
        upsert_settings(user_id, "course_id", answer[0])
        bot.send_message(user_id, f'Текущий выбранный курс: {text}')

        state.set_state(user_id, 'main')
        bot.send_message(
            user_id, 
            "Выбери пункт меню:", 
            reply_markup=markups.get_main_markup()
        )

    else:
        bot.send_message(
            user_id, 
            "Смена курса обучения:", 
            reply_markup=markups.get_course_markup()
        )

def _2_step_teacher_handler(bot, user_id: int, text: str):
    answer = course_answer(text)
    if answer:
        upsert_settings(user_id, "course_id", answer[0])
        bot.send_message(user_id, f'Текущий выбранный курс: {text}')

        state.set_state(user_id, 'main')
        bot.send_message(
            user_id, 
            "Выбери пункт меню:", 
            reply_markup=markups.get_teacher_main_markup()
        )

    else:
        bot.send_message(
            user_id, 
            "Смена курса обучения:", 
            reply_markup=markups.get_course_markup()
        )

def main_menu_handler(bot, user_id: int, text: str):
    if text == 'ℹ️ Модули':
        mrkp = markups.get_modules_markup(user_id)

        isEmpty = not mrkp.to_dict().get('inline_keyboard')
        
        text = "Выберите нужный модуль:"

        if isEmpty:
            text = "К сожалению доступных модулей для вашего языка и курса не найдено :("

        bot.send_message(user_id, text, reply_markup=mrkp)

    elif text == '⚙️ Настройки':
        state.set_state(user_id, 'settings')
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_main_markup())


def lang_menu_handler(bot, user_id: int, text: str):
    answer = lang_answer(text)
    if answer:
        set_user_lang(user_id, answer[0])
        bot.send_message(user_id, f'Текущий язык для обучения: {text}')

        state.set_state(user_id, 'settings')
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Смена языка обучения:", reply_markup=markups.get_lang_markup())


def course_menu_handler(bot, user_id: int, text: str):
    answer = course_answer(text)
    if answer:
        upsert_settings(user_id, "course_id", answer[0])
        bot.send_message(user_id, f'Текущий выбранный курс: {text}')

        state.set_state(user_id, 'settings')
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

    else:
        bot.send_message(user_id, "Смена курса обучения:", reply_markup=markups.get_course_markup())

def settings_menu_handler(bot, user_id: int, text: str):
    if text == "Изменить изучаемый язык":
        state.set_state(user_id, 'lang_menu')
        bot.send_message(user_id, "Смена языка обучения:", reply_markup=markups.get_lang_markup())
    
    elif text == "Изменить курс обучения":
        state.set_state(user_id, 'course_menu')
        bot.send_message(user_id, "Смена курса обучения:", reply_markup=markups.get_course_markup())

    elif text == "Изменить роль (тестовая функция)":
        state.set_state(user_id, 'roles')
        bot.send_message(user_id, "Выберите желаемую роль:", reply_markup=markups.get_roles_markup())
        
    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_settings_markup())

def roles_menu_handler(bot, user_id: int, text: str):
    answer = role_answer(text)
    if answer:
        update_role(user_id, answer[0])
        state.set_state(user_id, None)
        bot.send_message(user_id, "Ваша роль успешно изменилась", reply_markup=markups.get_next_markup())
        
    else:
        bot.send_message(user_id, "Выберите желаемую роль:", reply_markup=markups.get_roles_markup())

def module_menu_handler(bot, user_id: int, module_id: int):
    mrkp = markups.get_themes_markup(module_id)

    isEmpty = not mrkp.to_dict().get('inline_keyboard')

    text = "Выберите необходимую тему:"
    if isEmpty:
        text = "К сожалению доступных тем для данного модуля еще не добавили 😞"

    bot.send_message(user_id, text, reply_markup=mrkp)

def theme_menu_handler(bot, user_id: int, text: str, theme_id: int):
    user_state = str(state.get_state(user_id)).split('/')
    current_theme_id = user_state[1]
    current_exersise_id = user_state[2]

    if text != "Продолжить ➡️":
        save_answer(current_exersise_id, user_id, text)

    ex = get_exercise(current_theme_id, current_exersise_id)
    if not ex:
        grade = calc_result(bot, user_id)
        set_user_grade(user_id, theme_id, grade)
        state.set_state(user_id, 'main')
        return
    
    ExersiseFactory.create_exersise(ex, bot, user_id).send()

    next_exersise_id = ex[0]
    state.set_state(user_id, f"theme/{current_theme_id}/{next_exersise_id}")


def teach_main_menu_handler(bot, user_id: int, text: str):
    if text == 'ℹ️ Модули':
        mrkp = markups.get_modules_markup(user_id)

        isEmpty = not mrkp.to_dict().get('inline_keyboard')
        
        text = "Выберите нужный модуль:"

        if isEmpty:
            text = "К сожалению доступных модулей для вашего языка и курса не найдено 😞"

        bot.send_message(user_id, text, reply_markup=mrkp)

    elif text == "📊 Статистика оценок":
        text_stat = '<b>Статистика оценок по вашим модулям 📊:</b>\n\n'
        stat = get_teacer_stat(user_id)

        if not stat:
            bot.send_message(user_id, "Тестов по темам ваших модулей еще не решалось 😞")
            return

        for module_id, module_name, themes in stat:
            module_stat_text = f"<b>{module_name}</b>\n"

            for theme_data in themes:
                theme_stat_text = f"ㅤ<i>{theme_data.get('theme_name')}</i>\n"

                for grade in theme_data.get("grades_data"):
                    user = grade.get("user")
                    grade = grade.get("grade")
                    last_name = user.get('last_name')
                    name = user.get('name')
                    login = user.get('login')

                    user_alias = ""
                    if last_name:
                        user_alias += f"{last_name} "
                    if name:
                        user_alias += f"{name} "
                    if login:
                        user_alias += f"({login})"

                    grade_stat_text = f"ㅤㅤ{user_alias} - {grade}\n"

                    theme_stat_text += grade_stat_text

                theme_stat_text += '\n'
                module_stat_text += theme_stat_text

            module_stat_text += '\n'
            text_stat += module_stat_text

        bot.send_message(user_id, text_stat, parse_mode="HTML")

    elif text == '⚙️ Настройки':
        state.set_state(user_id, 'settings')
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_teacher_settings_markup())

    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_teacher_main_markup())


def admin_main_menu_handler(bot, user_id: int, text: str):
    if text == '⚙️ Настройки':
        state.set_state(user_id, 'settings')
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_teacher_settings_markup())

    elif text == '📊 Сводка о пользователях':
        u_text = "<b>Список пользователей</b>\n"

        for user in get_users():
            id, name, last_name, login, role, created_at = user
            user_alias = ""
            if last_name:
                user_alias += f"{last_name} "
            if name:
                user_alias += f"{name} "
            if login:
                user_alias += f"({login})"
            u_text += f"{user_alias} {role}. Создан: {created_at}\n"

        bot.send_message(user_id, u_text, parse_mode="HTML")

    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_admin_main_markup())

def teacher_settings_menu_handler(bot, user_id: int, text: str):
    if text == "Изменить роль (тестовая функция)":
        state.set_state(user_id, 'roles')
        bot.send_message(user_id, "Выберите желаемую роль:", reply_markup=markups.get_roles_markup())

    elif text == "⚙️ Редактировать":
        state.set_state(user_id, 'edit_module')
        bot.send_message(user_id, "Выберите действие с модулем:", reply_markup=markups.get_edit_module_markup())

    else:
        bot.send_message(user_id, "Выберите вариант из меню:", reply_markup=markups.get_teacher_settings_markup())


def edit_module_menu_handler(bot, user_id: int, text: str):
    if text == "➕ Создать модуль":
        state.set_state(user_id, 'create_module')
        bot.send_message(user_id, "Введите название нового модуля:", reply_markup=markups.remove_markup())

    elif text == "✏️ Изменить модуль":
        bot.send_message(user_id, "Выберите модуль для изменения:", reply_markup=markups.get_modules_markup(user_id))

    else:
        bot.send_message(user_id, "Выберите действие с модулем:", reply_markup=markups.get_edit_module_markup())


def edit_theme_menu_handler(bot, user_id: int, text: str, module_id: int = None):
    if text == "➕ Создать тему":
        module_id = str(state.get_state(user_id)).split("/")[1]
        state.set_state(user_id, f'create_theme/{module_id}')
        bot.send_message(user_id, "Введите название новой темы:", reply_markup=markups.remove_markup())

    elif text == "✏️ Изменить тему":
        bot.send_message(user_id, "Выберите тему для изменения:", reply_markup=markups.get_themes_markup(module_id))

    else:
        bot.send_message(user_id, f"Выберите действие с темой:", reply_markup=markups.get_edit_theme_markup())


def create_handler(bot, user_id: int, text: str, create_type: str, parent_id: int = None):
    if create_type == "module":
        state.set_state(user_id, 'edit_module')
        bot.send_message(user_id, f"Создан модуль: {text}", reply_markup=markups.get_next_markup())

    elif create_type == "theme":
        state.set_state(user_id, f'edit_module/{parent_id}')
        bot.send_message(user_id, f"Создана тема: {text} у модуля с id = {parent_id}", reply_markup=markups.get_next_markup())

    elif create_type == "exersise":
        state.set_state(user_id, f'edit_theme/{parent_id}')
        bot.send_message(user_id, f"Создано упражнение: {text} у темы с id = {parent_id}", reply_markup=markups.get_next_markup())


def edit_module_handler(bot, user_id: int, text, module_id: int = None):
    if text == "✏️ Изменить название":
        module_id = str(state.get_state(user_id)).split("/")[1]
        state.set_state(user_id, f'change_module_name/{module_id}')
        bot.send_message(user_id, f"Введите новое название модуля:", reply_markup=markups.remove_markup())
    
    elif text == "❌ Удалить":
        module_id = str(state.get_state(user_id)).split("/")[1]
        delete_module(module_id)
        bot.send_message(user_id, f"Модуль удален", reply_markup=markups.get_back_markup())

    elif text == "Редактировать содержимое":
        state.set_state(user_id, f'edit_module_child/{module_id}')
        edit_theme_menu_handler(bot, user_id, None)
        
    else:
        if module_id:
            state.set_state(user_id, f'edit_module/{module_id}')

        bot.send_message(user_id, f"Выберите действие с модулем:", reply_markup=markups.get_edit_object_markup())


def edit_theme_handler(bot, user_id: int, text, theme_id: int):
    if text == "✏️ Изменить название":
        theme_id = str(state.get_state(user_id)).split("/")[1]
        state.set_state(user_id, f'change_theme_name/{theme_id}')
        bot.send_message(user_id, f"Введите новое название темы:", reply_markup=markups.remove_markup())
    
    elif text == "❌ Удалить":
        theme_id = str(state.get_state(user_id)).split("/")[1]
        delete_theme(theme_id)
        bot.send_message(user_id, f"Тема удалена", reply_markup=markups.get_back_markup())

    elif text == "Редактировать содержимое":
        state.set_state(user_id, f'edit_theme_child/{theme_id}')
        edit_exersises_menu_handler(bot, user_id, text, theme_id)
        
    else:
        if theme_id:
            state.set_state(user_id, f'edit_theme/{theme_id}')

        bot.send_message(user_id, f"Выберите действие с темой:", reply_markup=markups.get_edit_object_markup())

def change_name(bot, user_id: int, text: str, type: str, id: int):
    if type == "module":
        update_module(id, text)
        state.set_state(user_id, f'edit_module/{id}')
        bot.send_message(user_id, f"Название модуля изменено", reply_markup=markups.get_next_markup())

    elif type == "theme":
        update_theme(id, text)
        state.set_state(user_id, f'edit_theme/{id}')
        bot.send_message(user_id, f"Название темы изменено", reply_markup=markups.get_next_markup())

def edit_exersises_menu_handler(bot, user_id: int, text: str, theme_id: int = None):
    if text == "➕ Создать упражнение":
        # theme_id = str(state.get_state(user_id)).split("/")[1]
        state.set_state(user_id, f'create_exersise/{theme_id}')
        bot.send_message(user_id, "Введите название нового упражнения:", reply_markup=markups.remove_markup())

    elif text == "✏️ Изменить упражнение":
        bot.send_message(user_id, "Выберите упражнение для изменения:", reply_markup=markups.get_exersises_markup(theme_id))

    else:
        bot.send_message(user_id, f"Выберите действие", reply_markup=markups.get_edit_exersises_markup())
        
def edit_exersise_handler(bot, user_id: int, text, exersise_id: int):
    if text == "✏️ Изменить заголовок":
        bot.send_message(user_id, "Изменение заголовка")
    
    elif text == "✏️ Изменить контент":
        bot.send_message(user_id, "Изменение контента")
