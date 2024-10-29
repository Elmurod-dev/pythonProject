from datetime import datetime

from aiogram import html, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.inline import channel_link
from bot.buttons.reply import generate_btn, send_contact_btn
from bot.dispacher import dp
from bot.state_ import UserRegisterState, MessageState
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from db.models import User, Message_to_admin

main_router = Router()
@main_router.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    user = await User.get_user(id_=message.from_user.id)
    if user:
        n = ["💳 Mening imtiyoz kartam", "🛍 Заказать на сайте", "⚙️ Sozlamalar", "📍 Do'konlarimiz",
             "✍️ Оставить отзыв", "☎️ Связаться с нами", "💼 Вакансии", "🔄 Условия возврата/обмена"]
        d = (1, 1, 2, 2, 2,)
        await message.answer(text=_("Menu"),reply_markup=generate_btn(n,d))
    else:
        text = """Здравствуйте! 🌟 Давайте для начала выберем язык обслуживания! 🌐

        Assalomu aleykum! 🌟 Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik. 🌐

        Choose a language, please"""
        await state.set_state(UserRegisterState.lang)
        name = ["🇷🇺 Русский", "🇺🇿 O'zbek", ""]
        design = (2,)
        await message.answer(text=text, reply_markup=generate_btn(btn_names=name, design=design))


@main_router.message(F.text.in_(["🇷🇺 Русский","🇺🇿 O'zbek"]),UserRegisterState.lang)
async def command_start_handler(message: Message,state:FSMContext) -> None:
    await state.update_data(lang = "ru" if message.text == "🇷🇺 Русский" else 'uz')
    await state.set_state(UserRegisterState.phone)
    await message.answer(text=_("Telefon raqamni yuborish"),reply_markup=send_contact_btn())


@main_router.message(lambda message: message.contact is not None)
async def handle_contact(message: Message,state:FSMContext):
    await state.update_data(phone = message.contact.phone_number)
    await state.set_state(UserRegisterState.city)
    names= ["Farg'ona","Andijon","Namangan","Karshi","Toshkent","Samarqand","Jizzax","Qo'qon","Navoiy","Nukus","⬅️ orqaga"]
    d = (2,)
    await message.answer(text=_("Shaharni tanlang!"),reply_markup=generate_btn(names,d))


@main_router.message(F.text.in_(["Farg'ona","Andijon","Namangan","Karshi","Toshkent","Samarqand","Jizzax","Qo'qon","Navoiy","Nukus"]))
async def handle_contact(message: Message,state:FSMContext):
    await state.update_data(city = message.text)
    await state.set_state(UserRegisterState.jinsi)
    names= ["👨‍ Erkak","👩‍ Ayol","⬅️ orqaga"]
    d = (2,1)
    await message.answer(text=_("Jinsingizni ko'rsating:"),reply_markup=generate_btn(names,d))

@main_router.message(F.text.in_(["👨‍ Erkak","👩‍ Ayol"]))
async def handle_contact(message: Message,state:FSMContext):
    await state.update_data(jinsi = message.text)
    await state.set_state(UserRegisterState.full_name)
    await message.answer(text=_("Ismi Sharifi  familiyasini yuboring"))


@main_router.message(UserRegisterState.full_name)
async def handle_contact(message: Message,state:FSMContext):
    await state.update_data(full_name = message.text)
    await state.set_state(UserRegisterState.date)
    await message.answer(text=_("Tug'ulgan yil,oy, sana(misol: 01-01-1993)"))

@main_router.message(UserRegisterState.date)
async def handle_contact(message: Message,state:FSMContext):
    try:
        result = datetime.strptime(message.text,"%Y-%m-%d")
        await state.update_data(date=result)
        data = await state.get_data()
        await User.create(full_name=data['full_name'],city=data['city'],
                            jinsi=data['jinsi'],
                            date=data['date'],
                            lang=data['lang'],
                            phone_number=data['phone'],
                            user_id=message.from_user.id)
        await state.clear()
        n = ["💳 Mening imtiyoz kartam","🛍 Заказать на сайте","⚙️ Sozlamalar","📍 Do'konlarimiz",
             "✍️ Оставить отзыв","☎️ Связаться с нами","💼 Вакансии","🔄 Условия возврата/обмена"]
        d = (1,1,2,2,2,)
        await message.answer(text=_(f"""{message.from_user.full_name}, Мы рады видеть вас в числе наших покупателей. С помощью этого бота вы можете:

- Пользоваться накопительной картой, проверить баланс и историю карты, использовать ее при   следующей покупки, показав штрих-код кассиру. 💳🛍️
- Оставлять отзыв или обратную связь 💬
- Заказать доставку одежды не выходя из телеграма 🚚👕
- Быть в курсе новых поступлений и эксклюзивных акций. 🛒💰
- Узнать адреса и контакты наших магазинов. 📍📞
- Получить информацию по актуальным вакансиям в нашей компании. 💼👔"""),reply_markup=generate_btn(n,d))
    except ValueError as e:
        await state.set_state(UserRegisterState.date)
        await message.answer(text=_("Tug'ulgan yil,oy, sana(misol: 01-01-1993)"))


@main_router.message(F.text == "💳 Mening imtiyoz kartam")
async def handle_contact(message: Message,state:FSMContext):
    url = "https://t.me/terraprowoman"
    await message.answer(text=_("Для получения информации о вашей накопительной карте 💳, пожалуйста, подпишитесь на наш телеграм-канал 📢"),reply_markup=channel_link(url))



@main_router.message(F.text == "🛍 Заказать на сайте")
async def handle_contact(message: Message,state:FSMContext):
    url = "https://terrapro.uz/?utm_source=tgbot&utm_medium=knopka&utm_campaign=tgbot"
    await message.answer(text=_("Для заказа, нажмите на кнопку Перейти на сайт (https://terrapro.uz/?utm_source=tgbot&utm_medium=knopka&utm_campaign=tgbot)"),reply_markup=channel_link(url))

@main_router.message(F.text == "✍️ Оставить отзыв")
async def handle_contact(message: Message,state:FSMContext):
    await state.set_state(MessageState.msg)
    await message.answer(text=_("Agar biror muammoga duch kelgan bo'lsangiz, iltimos, uni imkon qadar batafsilroq yoriting."))


@main_router.message(MessageState.msg)
async def handle_contact(message: Message,state:FSMContext):
    await state.update_data(msg = message.text)
    await Message_to_admin.create(text = message.text)
    await state.clear()
    await message.answer(text=_("Rahmat! Fikringiz tez orada ko'rib chiqiladi"))

@main_router.message(F.text == "💼 Вакансии")
async def handle_contact(message: Message,state:FSMContext):
    text = """Стань частью нашей дружной семьи TerraPro😇

Переходи в бот https://t.me/TerraPro_jbot или же позвони по номеру +998 90 968 47 42 и присоединяйся к нам."""
    url = "https://t.me/TerraPro_jbot"
    await message.answer(text=text,reply_markup=channel_link(url))



@main_router.message(F.text == __("🔄 Условия возврата/обмена"))
async def handle_contact(message: Message,state:FSMContext):
    text = """Правила обмена и возврата товара.

В соответствии с законом Республики Узбекистан «О защите прав потребителей» покупатель имеет право вернуть или обменять товар надлежащего качества в течении 10 дней со дня приобретения товара, если товар не был в употреблении (т.е. обувь или одежда не ношена), сохранен его товарный вид (отсутствуют любого рода повреждения), сохранены ярлыки, а также документ, подтверждающий факт приобретения товара (товарный или электронный чек).

Если товар не соответствует вышеуказанным требованиям, в таком случае товар возврату и обмену не подлежит. Так же не подлежат возврату носочно-чулочные изделия и нательное белье. 

Потребитель вправе в течение 10 дней со дня покупки обменять товар ненадлежащего качества (производственный брак, товар несоответствующий качеству) на аналогичный в том магазине, где он был приобретен, а в случае отсутствия аналогичного товара в продаже — получить возврат денежных средств."""
    await message.answer(text=text)









