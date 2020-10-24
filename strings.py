# TODO: Добавить маркированный текст и какой-то дизайн
from aiogram.utils.markdown import text, bold
from enum import Enum


class ReminderState(Enum):
    R_FALSE = 'Не нуждается в измении',
    R_DO = 'За изменения взялся',
    R_TRUE = 'Нужно изменить'

    def __init__(self, description):
        self.description = description


class Reminder:
    def __init__(self, command, description):
        self.command = command
        self.description = description


# TODO: перевести в Enum
reminders_start = {
    'schedule': Reminder('schedule', text(f"Необходимо внести изменения в {bold('Google Calendar')}.",
                                          "Данное сообщение будет повторяться каждые 15 минут.",
                                          "Для отключения необходимо ввести /done_schedule.", sep='\n')),
    'homework': Reminder('homework', text("Необходимо внести изменения в Trello.",
                                          "Данное сообщение будет повторяться каждые 15 минут.",
                                          "Для отключения необходимо ввести /done_homework", sep='\n'))
}

reminders_state = {
    'schedule': Reminder('is_schedule', "Состояние Google Calendar:"),
    'homework': Reminder('is_homework', "Состояние Trello:")
}

reminders_make = {
    'schedule': Reminder('make_schedule', "За внесения поправок в Google Calendar взялся - "),
    'homework': Reminder('make_homework', "За внесения изменений в Trello взялся - ")
}

reminders_stop = {
    'schedule': Reminder('done_schedule', text("Google Calendar:",
                                               "Повтор напоминаний отключен.", sep='\n')),
    'homework': Reminder('done_homework', text("Trello:",
                                               "Повтор напоминаний отключен.", sep='\n'))
}

bs_command = 'build_server'

help_command = 'help'
help_text = text('**Google Calendar**',
                 '/schedule - Напоминание о внесения изменений в Google Calendar',
                 '/is_schedule - Нужно ли вносить изменения в Google Calendar?',
                 '/make_schedule - Я берусь за изменения в Google Calendar',
                 '/done_schedule - Отключение напоминаний об изменений в Google Calendar',
                 '**Trello**',
                 '/homework - Напоминание о внесения изменений в Trello',
                 '/is_homework - Нужно ли вносить изменения в Trello?',
                 '/make_homework - Я берусь за изменения в Trello',
                 '/done_homework - Отключение напоминаний об изменений в Trello',
                 '**Build Server Python**',
                 '/build_server - Build Server и задачки по Python', sep='\n')
