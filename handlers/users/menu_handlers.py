from aiogram import types
from loader import dp, db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.default.start_keyboard import menu,menu_2
from aiogram.dispatcher import FSMContext
from utils.misc.product import Product
from aiogram.utils.callback_data import CallbackData

basket_item_action = CallbackData("buy", "item_action", "product")



@dp.message_handler(text='🛍 Mahsulotlar',state=None)
async def bot_categories(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    
    products = await db.get_categories()
    await state.set_state("product")
    
    for i in range(0,len(products)-1):
        for i in range(0,len(products)-1,2):
            markup.row(KeyboardButton(text=f"{products[i][0]}"),KeyboardButton(text=f"{products[i+1][0]}"))
            
        if len(products)%2==1:
            markup.row(KeyboardButton(text=f"{products[len(products)-1][0]}"))
        markup.row(KeyboardButton(text="⬅️Ortga"))
    

    await message.answer(text='Kategoriyani tanlang.',reply_markup=markup)





@dp.message_handler(state='product')
async def bot_echos(message: types.Message, state: FSMContext):
    markup1 = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    if message.text == '⬅️Ortga':
        await message.answer('Asosiy meyu',reply_markup=menu)
        await state.finish()
    else:
        await state.set_state("product_name")
        products = await db.get_products(message.text)
        product_name=products
        await state.update_data(
            {"products": message.text}
        )
    
        for i in range(0,len(product_name)-1,2):
            markup1.row(KeyboardButton(text=f"{product_name[i][2]}"),KeyboardButton(text=f"{product_name[i+1][2]}"))
        if len(product_name)%2==1:
            markup1.row(KeyboardButton(text=f"{product_name[len(product_name)-1][2]}"))
        markup1.row(KeyboardButton(text="⬅️Ortga"))

        await message.answer(text='Kategoriyani tanlang.',reply_markup=markup1)
        

@dp.message_handler(state='product_name')
async def bot_echo(message: types.Message, state: FSMContext):
    if message.text == '⬅️Ortga':
        markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        
        products = await db.get_categories()
        await state.set_state("product")
        
        for i in range(0,len(products)-1):
            for i in range(0,len(products)-1,2):
                markup.row(KeyboardButton(text=f"{products[i][0]}"),KeyboardButton(text=f"{products[i+1][0]}"))
                
            if len(products)%2==1:
                markup.row(KeyboardButton(text=f"{products[len(products)-1][0]}"))
            markup.row(KeyboardButton(text="⬅️Ortga"))

        await message.answer(text='Kategoriyani tanlang.',reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        await state.set_state("product_number")
        product = await db.get_product_name(message.text)
        product_id = product[0]
        product_name =product[2]
        await state.update_data(
            {"product_id": product_id}
        )
        await state.update_data(
            {"product_name": product_name}
        )
        
        photo = product[3]
        caption =f'<b>{product_name}</b>\nNarxi:{product[4]}$\n<i>{product[5]}</i>'
        await message.answer_photo(photo=photo,reply_markup=menu_2,caption=caption)
        

@dp.message_handler(state='product_number')
async def bot_echo(message: types.Message, state: FSMContext):
    if message.text == '⬅️Ortga':
        markup1 = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
        
        data = await state.get_data()
        texts = data.get("products")
        products = await db.get_products(texts)
        product_name=products
        await state.set_state("product_name")
    
        for i in range(0,len(product_name)-1,2):
            markup1.row(KeyboardButton(text=f"{product_name[i][2]}"),KeyboardButton(text=f"{product_name[i+1][2]}"))
        if len(product_name)%2==1:
            markup1.row(KeyboardButton(text=f"{product_name[len(product_name)-1][2]}"))
        markup1.row(KeyboardButton(text="⬅️Ortga"))

        await message.answer(text='Mahsulotni tanlang.',reply_markup=markup1)
    else:
        data = await state.get_data()
        
        
        user_id=message.from_user.id
        product_id = data.get("product_id")
        product_name = data.get("product_name")
        
        
        if message.text == 'Asosiy menyu':
            await message.answer('Asosiy meyu',reply_markup=menu)
            await state.finish()
        await state.finish()
        try:
            await db.add_basket(user_id=user_id,product_id=product_id,count=int(message.text),productname=product_name)
        except:
            await db.update_count_pr(int(message.text),product_id)
            await db.update_pr_name(product_name,product_id)

            
        await message.answer(text='Mahsulot savatchaga qo\'shildi',reply_markup=menu)

        
    
    
@dp.message_handler(text='Asosiy menyu')
async def bo_categories(message: types.Message):
    await message.answer('Asosiy meyu',reply_markup=menu)

       
@dp.message_handler(text="🛒 Savatcha")
async def show_bascket(message: types.Message):
    idw = await db.get_baskets(user_id=message.from_user.id)
    a=''
    total=0
    for i in idw:
        product=await db.get_product(int(i[2]))
        count=int(i[3])
        price =int(product[4])
        price_count =price*count
        total+=price_count
        a+=f'{product[2]}\n{count}*{price} = {price_count}\nUmumiy narx: {total} $\n\n'

    if a=='':
            await message.answer(text="Xozir siz hech qanday mahsulot tanlamadingiz!") 
    else:
        markup = action_keyboard(idw)
        await message.answer(a, reply_markup=markup)
    


def action_keyboard(idw):
    inline_markup = InlineKeyboardMarkup(row_width=4)
    for i in idw:
        
        inline_markup.add(InlineKeyboardButton(text=i[4], callback_data="1"), 
            InlineKeyboardButton(text="➕", callback_data=basket_item_action.new(item_action="plus", product=i[2])), 
            InlineKeyboardButton(text="❌", callback_data=basket_item_action.new(item_action="delete", product=i[2])), 
            InlineKeyboardButton(text="➖", callback_data=basket_item_action.new(item_action="minus", product=i[2]))),
    inline_markup.add(InlineKeyboardButton(text="🛒 Savatchani bo'shatish!", callback_data=basket_item_action.new(item_action="deletebsk",product=i[2])))
    inline_markup.add(InlineKeyboardButton(text="Buyurtma berish!", callback_data=basket_item_action.new(item_action="order",product=i[2])))
    return inline_markup
