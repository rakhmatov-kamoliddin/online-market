import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from filters.PrivateFilter import IsPrivate
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.start_keyboard import menu



@dp.message_handler(text="/addproduct")
async def add_product(message: types.Message, state: FSMContext):
    await state.set_state("addcategory")
    category = await db.get_categories()
    keyboard_category=[]
    for i in category:
        keyboard_category.append([KeyboardButton(text=i[0])])
        
    category_markup = ReplyKeyboardMarkup(
    keyboard_category,
    resize_keyboard=True,
)
    await message.answer("Categoryni kiriting...",reply_markup=category_markup)





@dp.message_handler(state = "addcategory", content_types=types.ContentType.TEXT)
async def add_category(message: types.Message, state: FSMContext):
    category = message.text

    await state.update_data(
        {"category": category}
    )
    await state.set_state("addproductname")
    
    
    await message.answer("Productnameni kiriting...",reply_markup=ReplyKeyboardRemove())
    



@dp.message_handler(state = "addproductname", content_types=types.ContentType.TEXT)
async def add_addproductname(message: types.Message, state: FSMContext):
    productname = message.text
    await state.set_state("addproductphoto")
    await state.update_data(
        {"productname": productname}
    )
    await message.answer("Product photoni kiriting...")
    




@dp.message_handler(state = "addproductphoto", content_types=types.ContentType.PHOTO)
async def add_addproductphoto(message: types.Message, state: FSMContext):
    productphotoid = message.photo[-1].file_id
    
    await state.set_state("addproductprice")
    await state.update_data(
        {"productphotoid": productphotoid}
    )
    await message.answer("Product price kiriting...")


@dp.message_handler(state = "addproductprice", content_types=types.ContentType.TEXT)
async def add_addproductprice(message: types.Message, state: FSMContext):
    addproductprice = message.text
    await state.set_state("addproductdescription")
    await state.update_data(
        {"productprice": addproductprice}
    )
    await message.answer("Product description kiriting...")
    


@dp.message_handler(state = "addproductdescription", content_types=types.ContentType.TEXT)
async def add_addproductprice(message: types.Message, state: FSMContext):
    addproductdescription = message.text
    await state.update_data(
        {"productdescription": addproductdescription}
    )
    
    data = await state.get_data()
    category = data.get("category")
    
    product_name = data.get("productname")
    product_photo_id = data.get("productphotoid") 
    product_price = int(data.get("productprice"))
    product_description = data.get("productdescription") 
    await state.finish()
    
    await db.add_product(
        category,
        product_name,
        product_photo_id,
        product_price,
        product_description,
    )
    
    
    await message.answer("Product muvaffaqiyatli qo'shildi")

    
    text = f"<a href=\"{product_photo_id}\">{product_name}</a>\n\n"
    text += f"Narxi: {product_price}$\n{product_description}"

    await message.answer_photo(photo=product_photo_id,caption=text,reply_markup=menu)






@dp.message_handler(IsPrivate(), text="/advert", user_id=ADMINS)
async def send_ad_command(message: types.Message, state: FSMContext):
    await message.answer("Отправьте рекламу...")
    await state.set_state("advertisement")


@dp.message_handler(state = "advertisement", content_types=types.ContentType.ANY)
async def sending_advert(message: types.Message, state: FSMContext):
    state.finish()
    users = db.select_all_users()
    count = db.count_users()[0]
    
    for user in users:
        user_id = user[0]
    await bot.copy_message(user_id, message.chat.id, message.message_id)
    await message.answer(f"Реклама была отправлена {count} пользователям.")
    await state.finish()


@dp.message_handler(Command('touser'))
async def bot_echo(message: types.Message, state: FSMContext):
    
    await message.answer('Savol va e\'tirozlaringizni kiriting')
    
    await state.set_state("touser")

@dp.message_handler(state="touser")
async def enter_email(message: types.Message, state: FSMContext):
    from_chat_id=message.from_id
    message_id=message.message_id
    msg = message.text
    await state.finish()
    await bot.forward_message(chat_id=ADMINS[0], from_chat_id=from_chat_id,message_id=message_id)


@dp.message_handler(text="/deletedb")
async def send_ad_command(message: types.Message):
    await db.drop_products()


@dp.message_handler(text="/deletebsk")
async def send_ad_command(message: types.Message):
    await db.drop_basket()
    await db.create_table_basket()
    await message.answer('Savatcha tozalandi')
    

