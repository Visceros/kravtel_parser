#coding: utf-8

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
#from aiogram.dispatcher.filters import Text
import os

bot = Bot(token="5542925253:AAFxetzsyGU0uv_poJ1BSTQiKzV0dvyY5c4")
dp = Dispatcher(bot)
start_message_image = types.InputFile(os.path.join(os.getcwd(), 'Mantera_photo.png'))
presentation = types.InputFile(os.path.join(os.getcwd(), 'Mantera_29062022.pdf'))

# Здесь нужно указать чат, куда будут присылаться контакты с просьбами перезвонить и т.п.
operator_chat = 'https://t.me/Visceros90'

btn_callback = types.reply_keyboard.KeyboardButton(text='Заказать звонок')
btn_chat = types.reply_keyboard.KeyboardButton(text='Чат со специалистом', url='')
btn_presentation = types.reply_keyboard.KeyboardButton(text='Получить презентацию')
btn_come_to_see = types.reply_keyboard.KeyboardButton(text='Виртуальный тур')
menu = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(btn_callback, btn_chat, btn_presentation,btn_come_to_see)

ask_phone = types.reply_keyboard.ReplyKeyboardMarkup()
ask_phone_btn = types.reply_keyboard.KeyboardButton(request_location=True, text='Отправить номер телефона', callback_data='Телефон отправлен')
ask_phone.add(ask_phone_btn)

# Добавить фильтр на сообщения вместо лямбды??: https://aiogram-birdi7.readthedocs.io/en/latest/dispatcher/filters.html


greetings_message = f'Комплекс deluxe-класса MANTERA Seaview residence расположен на первой линии моря на фоне уникального природного ландшафта, свойственного только Сочи. Комплекс формируют величественные здания, устремленные фасадами к восходящему солнцу 🔅! Благоустроенная территория более 10 гектаров с объектами отдыха и развлечений.\n\nС нами можно связаться по номеру 📞 8 (800) 300-61-49. Фото комплекса:'

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.message):
	await message.answer(f'Добрый день {message.from_user.first_name}! Это чат-бот Mantera Seaview Residence, '
						 f'мы на связи!\n \n {greetings_message}', reply_markup=menu)
	await bot.send_photo(chat_id=message.from_user.id, photo=start_message_image)

@dp.message_handler(lambda message: 'Заказать звонок' == message.text)
async def ask_callback(message:types.message):
	await message.answer(f"Для заказа звонка, пожалуйста, оставьте ваш номер телефона.", reply_markup=ask_phone)
	# В чат оператора нужно отправить сообщение, что такому-то (user.full_name) номер телефона:{phoneNumber}, нужно перезвонить

# Что случится при нажатии кнопки Получить презентацию:
@dp.message_handler(lambda message: 'Получить презентацию' == message.text)
async def ask_presentation(message:types.message):
	await message.answer(f"Для получения презентации, пожалуйста, оставьте ваш номер телефона.", reply_markup=ask_phone)
	# Тут нужно проверить, что человек оставил номер телефона и отправить ему презентацию.
	# А в чат оператора отправить сообщение, что такой-то (user.full_name) номер телефона:{phoneNumber}, запросил презентацию


@dp.message_handler(lambda message: 'Виртуальный тур' == message.text)
async def ask_presentation(message:types.message):
	await message.answer(f"Для записи на просмотр, пожалуйста, оставьте ваш номер телефона.", reply_markup=ask_phone)
# Тут нужно проверить, что человек оставил номер телефона и отправить ему ссылку.
# А в чат оператора отправить сообщение, что такой-то (user.full_name) номер телефона:{phoneNumber}, запросил виртуальный тур
# ссылка на виртуальный тур: 'https://tour.virtualland.ru/svl/mantera-residence/'


@dp.message_handler(content_types=['contact'])
async def get_contact(message):
	if message.contact is not None:
		global phoneNumber
		global forward_user_id
		phoneNumber= str(message.contact.phone_number)
		forward_user_id = str(message.contact.user_id)

executor.start_polling(dp, skip_updates=True)