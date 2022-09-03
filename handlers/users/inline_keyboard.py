from distutils.cmd import Command
from sre_parse import State
from filters.PrivateFilter import IsPrivate
from data.config import ADMINS
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton
from aiogram import types
from keyboards.default.start_keyboard import menu
from aiogram.dispatcher.filters.builtin import Text,Command
from keyboards.inline import OurInlineKeyboard
from loader import dp
from aiogram.dispatcher import FSMContext

@dp.message_handler(Text("Ko'proq..."))
async def bot_start(message: types.Message):
    await message.answer(f"Adminga murojat qilish!",reply_markup=OurInlineKeyboard.Courses)
    
@dp.callback_query_handler(text="admin")
async def bot_text_to_admin(call: types.CallbackQuery,state: FSMContext):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.row(KeyboardButton(text="⬅️Ortga"))
    await call.message.answer(f"Iltimos, xabaringizni kiriting..", reply_markup=markup)
    await state.set_state("feetback")

@dp.message_handler(state = "feetback")
async def text_to_admin(message: types.Message, state: FSMContext):
    if message.text=="⬅️Ortga":
        await message.answer(text="Asosiy menyu", reply_markup=menu)
    else:    
        await message.answer("Sizning xabaringiz qabul qilindi. Xabar jo'natib bizni rivojlanishimizga yordam berayotganingiz uchun <b>raxmat</b>!", reply_markup=menu)
        for admin in ADMINS:
            await dp.bot.send_message(admin, f"Foydalanuvchi sizga murojat qildi.\nIsmi:@{message.from_user.username}\nMurojat:\t{message.text}")
    await state.finish()
    
    
    
@dp.message_handler(Command('developer'))
async def online_course(message: types.Message):
    await message.answer('🇺🇿Dasturchi: @rakhmat0v_2007')
    
    
@dp.message_handler(Text("/admin"), IsPrivate())
async def bot_text_to_admin(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.row(KeyboardButton(text="⬅️Ortga"))
    await message.answer(f"Iltimos, xabaringizni kiriting..", reply_markup=markup)
    await state.set_state("feetback")

@dp.message_handler(state = "feetback")
async def text_to_admin(message: types.Message, state: FSMContext):
    if message.text=="⬅️Ortga":
        await message.answer(text="Asosiy menyu", reply_markup=menu)
    else:    
        await message.answer("Sizning xabaringiz qabul qilindi. Xabar jo'natib bizni rivojlanishimizga yordam berayotganingiz uchun <b>raxmat</b>!", reply_markup=menu)
        for admin in ADMINS:
            await dp.bot.send_message(admin, f"Foydalanuvchi sizga murojat qildi.\nIsmi:@{message.from_user.username}\nMurojat:\t{message.text}")
    await state.finish()