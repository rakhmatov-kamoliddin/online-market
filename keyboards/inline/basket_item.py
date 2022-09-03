from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db 

basket_item_action = CallbackData("buy", "item_action", "product")

async def basket_inline_keyboard(user_id):

    inline_markup = InlineKeyboardMarkup(row_width=4)
    products = await db.get_baskets(user_id)
    for i in products:
        
        inline_markup.row(InlineKeyboardButton(i[1]), 
            InlineKeyboardButton(text="+", callback_data=basket_item_action.new(item_action="plus", product=i[1])), 
            InlineKeyboardButton(text="-", callback_data=basket_item_action.new(item_action="minus", product=i[1])), 
            InlineKeyboardButton(text="x", callback_data=basket_item_action.new(item_action="delete", product=i[1])))
    inline_markup.row(InlineKeyboardButton(text="Buyurtma berish", callback_data=basket_item_action.new(item_action="order")))


    return inline_markup