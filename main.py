import config
import logging
import keyboards
from strings import reminders_start, reminders_stop, ReminderState, reminders_state, reminders_make, \
                    bs_command, \
                    help_command, help_text
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text


# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)


# команда \help
@dp.message_handler(commands=[help_command])
async def cmd_reminder_on(message: types.Message):
    await message.answer(help_text)


# МОДУЛЬ 1. Команды об напоминамий
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# переменные для хранения состояния включенности уведомлений для Trello и Google Calendar
# TODO: исправить этот костыль в будущем
is_schedule_reminder = False
is_homework_reminder = False


# Команды активации цикличного напоминания для Google Calendar и Trello.
# TODO: сделать ассинхронными потоками без глобальных переменных
@dp.message_handler(commands=[reminders_start['schedule'].command, reminders_start['homework'].command])
async def cmd_reminder_on(message: types.Message):
    if message.get_command(pure=True) == reminders_start['schedule'].command:
        global is_schedule_reminder
        if is_schedule_reminder:
            await message.answer('Уже включено')
            return
        await message.answer(reminders_start['schedule'].description)
        is_schedule_reminder = True
        while is_schedule_reminder:
            await asyncio.sleep(config.REMINDER_TIMER)
            if is_schedule_reminder:
                await message.answer(reminders_start['schedule'].description)
    elif message.get_command(pure=True) == reminders_start['homework'].command:
        global is_homework_reminder
        if is_homework_reminder:
            await message.answer('Уже включено')
            return
        await message.answer(reminders_start['homework'].description)
        is_homework_reminder = True
        while is_homework_reminder:
            await asyncio.sleep(config.REMINDER_TIMER)
            if is_homework_reminder:
                await message.answer(reminders_start['homework'].description)


# Команда просмотра состояния для Google Calendar и Trello.
@dp.message_handler(commands=[reminders_state['schedule'].command, reminders_state['homework'].command])
async def cmd_reminder_state(message: types.Message):
    msg_responsible = 'Нет ответственного'
    if message.get_command(pure=True) == reminders_state['schedule'].command:
        global is_schedule_reminder
        msg = reminders_state['schedule'].description
        if is_schedule_reminder:
            file_name = "responsible_in_schedule.txt"
            with open(file_name, 'r') as text_file:
                text_responsible = text_file.read()
                if text_responsible != '\n':
                    msg_state = ReminderState.R_DO.description
                    msg_responsible = f'@{text_responsible}'
                else:
                    msg_state = ReminderState.R_TRUE.description
        else:
            msg_state = ReminderState.R_FALSE.description
    elif message.get_command(pure=True) == reminders_state['homework'].command:
        global is_homework_reminder
        msg = reminders_state['homework'].description
        if is_homework_reminder:
            file_name = "responsible_in_homework.txt"
            with open(file_name, 'r') as text_file:
                text_responsible = text_file.read()
                if text_responsible != '\n':
                    msg_state = ReminderState.R_DO.description
                    msg_responsible = f'@{text_responsible}'
                else:
                    msg_state = ReminderState.R_TRUE.description
        else:
            msg_state = ReminderState.R_FALSE.description
    await message.answer(text(msg, msg_state, msg_responsible, sep='\n'))


# Команда за взятие ответственночти изменений для Google Calendar и Trello.
@dp.message_handler(commands=[reminders_make['schedule'].command, reminders_make['homework'].command])
async def cmd_reminder_make(message: types.Message):
    if message.get_command(pure=True) == reminders_make['schedule'].command:
        global is_schedule_reminder
        if not is_schedule_reminder:
            await message.answer('Нет необхоимости в изменении')
            return
        file_name = 'responsible_in_schedule.txt'
        await message.answer(text('Благодарю! ', reminders_make['schedule'].description, f'@{message.from_user.username}'))
    elif message.get_command(pure=True) == reminders_make['homework'].command:
        global is_homework_reminder
        if not is_homework_reminder:
            await message.answer('Нет необхоимости в изменении')
            return
        file_name = 'responsible_in_homework.txt'
        await message.answer(text('Благодарю! ', reminders_make['homework'].description, f'@{message.from_user.username}'))
    with open(file_name, 'w') as text_file:
        print(message.from_user.username, file=text_file)


# Команда деактивации цикличного уведомления для Google Calendar и Trello.
# TODO: сделать ассинхронными потоками без глобальных переменных
@dp.message_handler(commands=[reminders_stop['schedule'].command, reminders_stop['homework'].command])
async def cmd_reminder_on(message: types.Message):
    if message.get_command(pure=True) == reminders_stop['schedule'].command:
        global is_schedule_reminder
        if not is_schedule_reminder:
            await message.answer("Напоминание в Google Calendar не включено")
            return
        is_schedule_reminder = False
        await message.answer(reminders_stop['schedule'].description)
        file_name = 'responsible_in_schedule.txt'
    elif message.get_command(pure=True) == reminders_stop['homework'].command:
        global is_homework_reminder
        if not is_homework_reminder:
            await message.answer("Напоминание в Trello не включено")
            return
        is_homework_reminder = False
        await message.answer(reminders_stop['homework'].description)
        file_name = 'responsible_in_homework.txt'
    with open(file_name, 'w') as text_file:
        print(file=text_file)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# МОДУЛЬ 2. Build Server для Python. Тут еще наши задачки будут храниться
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


@dp.message_handler(commands=[bs_command])
async def cmd_build_server(message: types.Message):
    await message.reply('Открыть проект или загрузить новый проект?', reply_markup=keyboards.inline_kb_open)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
