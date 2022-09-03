from aiogram import types
from loader import dp, db
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from handlers.users.menu_handlers import basket_item_action,action_keyboard
from keyboards.default.start_keyboard import menu
from utils.misc.product import Product
from aiogram.types import *

@dp.callback_query_handler(basket_item_action.filter())
async def basket_actions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):

    item_action=callback_data.get("item_action")
    item_name=callback_data.get("product")
    idw = await db.get_baskets(user_id=call.from_user.id)
    idw.sort()
    a=''
    if item_action=="plus":
        await db.plus_count(product_id=call.from_user.id, user_id=item_name)
        a=''
        total=0
        for i in idw:
            product=await db.get_product(int(i[2]))
            count=int(i[3])
            price =int(product[4])
            price_count =price*count
            total+=price_count
            a+=f'{product[2]}\n{count}*{price} = {price_count}\nUmumi narx : {total} $\n\n'
        markup = action_keyboard(idw)
        await call.message.edit_text(text=a, reply_markup=markup)


    elif item_action=="minus":
        await db.minus_count(product_id=call.from_user.id, user_id=item_name)
        a=''
        total=0
        for i in idw:
            product=await db.get_product(int(i[2]))
            count=int(i[3])
            price =int(product[4])
            price_count =price*count
            total+=price_count
            a+=f'{product[2]}\n{count}*{price} = {price_count}\n Umumiy narx: {total} $\n\n'
        markup = action_keyboard(idw)
        await call.message.edit_text(text=a, reply_markup=markup)

    
    elif item_action=="delete":
        await db.del_count(product_id=call.from_user.id, user_id=item_name)
        a=''
        total=0
        for i in idw:
            product=await db.get_product(int(i[2]))
            count=int(i[3])
            price =int(product[4])
            price_count =price*count
            total+=price_count
            a+=f'{product[2]}\n{count}*{price} = {price_count}\nUmumiy  narx : {total} $\n\n'
        
        if a=='':
            await call.message.edit_text(text="Xozir siz hech qanday mahsulot tanlamadingiz!")       
        else:
            markup = action_keyboard(idw)
            await call.message.edit_text(text=a, reply_markup=markup)

    elif item_action=="deletebsk":
        await db.drop_basket()
        await db.create_table_basket()
        await call.message.delete()

    elif item_action == "order":
        a=''
        total=0
        for i in idw:
            product=await db.get_product(int(i[2]))
            count=int(i[3])
            price =int(product[4])
            price_count =price*count
            total+=price_count
            a+=f'{product[2]}\n{count}*{price} = {price_count}\nUmumiy narx: {total} $\n\n'
        
        Contact = ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='☎ Contact', request_contact=True),
            ],
        ],
            resize_keyboard=True
        )
        
        await state.update_data(
        {"order": a}
    )
        await state.set_state("contact")
        await call.message.answer("Telefon raqamingizni kiriting",reply_markup=Contact)
        
@dp.message_handler(state='contact',content_types=types.ContentType.CONTACT)
async def my_contact(message: types.Message,state: FSMContext):
    contact = message.contact['phone_number']
    name = message.contact['first_name']
    await state.update_data(
        {"contact": contact}
        
    )
    await state.update_data({'name':name})
    
    await state.set_state("location")
    
    Location = ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='Location', request_location=True),
            ],
        ],
            resize_keyboard=True
        )
    await message.answer("Manzilingizni kiriting",reply_markup=Location)
            
@dp.message_handler(state='location',content_types=types.ContentType.LOCATION)
async def not_my_contact(message: types.Message,state: FSMContext):
    latitude=message.location['latitude']
    longtitude=message.location['longitude']
    
    await state.update_data({'latitude':latitude})
    await state.update_data({'longtitude':longtitude})
    
    await state.set_state('order_type')
    Order = ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='🚶‍♂️O\'zim olib ketaman'),
                KeyboardButton(text='📲 Yetkazib berish'),
            ],
        ],
            resize_keyboard=True
        )
    await message.answer("Yetkazib berish turini tanlang!",reply_markup=Order)

@dp.message_handler(state='order_type',content_types=types.ContentType.TEXT)
async def not_my_contact(message: types.Message,state: FSMContext):
    
    await state.update_data({'order_type':message.text})
    await db.delete_bsk(message.from_user.id)
    await message.answer("Buyurtmangiz qabul qilindi!",reply_markup=menu)
    data = await state.get_data()
    await state.finish()
    order = data.get("order")
    contact = data.get("contact")
    name = data.get("name")
    latitude=data.get('latitude')
    longtitude=data.get('longtitude')
    order_type=data.get('order_type')
    
    await dp.bot.send_message(ADMINS[0],f'<b>Buyurtma beruvchi</b>:  \'{name}\'      @{message.from_user.username}\n<b>Telefon raqami</b>:  {contact}\n<b>Manzili</b>:  {latitude}, {longtitude}\n<b>Yetkazib berish turi</b>:  {order_type}\n<b>Buyurtma berdi</b>: {order}')