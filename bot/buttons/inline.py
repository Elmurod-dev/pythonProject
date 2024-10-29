from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def channel_link(link):
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text=_("link"),url=link)
    )
    return ikb.as_markup()
