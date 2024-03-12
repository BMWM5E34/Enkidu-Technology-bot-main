from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

cmd_start_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Existing Client", callback_data='existing_client')],
    [types.InlineKeyboardButton(text="New Client", callback_data='new_client')]
])

Existing_Client_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Service", callback_data='service')],
    [types.InlineKeyboardButton(text="Accounting", callback_data='accounting')],
    [types.InlineKeyboardButton(text="❌", callback_data='main_menu')]
])

New_Client_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="IT", callback_data='it')],
    [types.InlineKeyboardButton(text="VOP", callback_data='vop')],
    [types.InlineKeyboardButton(text="Management Consultancy", callback_data='management_consultancy')],
    [types.InlineKeyboardButton(text="Marketing", callback_data='marketing')],
    [types.InlineKeyboardButton(text="❌", callback_data='main_menu')]
])

Budget_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="0-10k", callback_data='zero-ten')],
    [types.InlineKeyboardButton(text="10 - 100k", callback_data='ten-hundred')],
    [types.InlineKeyboardButton(text="100k +", callback_data='hundred+')],
    [types.InlineKeyboardButton(text="❌", callback_data='main_menu')]
])

