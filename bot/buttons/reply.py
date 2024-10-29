from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def generate_btn(btn_names , design):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=i) for i in btn_names])
    rkb.adjust(*design)
    return rkb.as_markup(resize_keyboard=True,one_time_keyboard=True)

def send_contact_btn():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_("📞 Send contact"),request_contact=True))
    return rkb.as_markup(resize_keyboard=True, one_time_keyboard=True)
