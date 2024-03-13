import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Other
import keyboard as kb
import config as cfg

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import os
import urllib.request

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    Interested = State()
    NewUserContact = State()
    Budget = State()

    customer_response = State()
    screenshot = State()
    ExistingClientInfo = State()

line = "-------------------------"

Sender = "ReportsEnkidu@outlook.com"

Sender_email_password = f"greyh5363"

Recipient = "clients@enkidutech.com"

async def send_email(subject, message, to_email, file_path=None):
    smtp_username = Sender
    smtp_password = Sender_email_password
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if file_path:
        with open(file_path, 'rb') as file:
            attachment = MIMEImage(file.read(), name=os.path.basename(file_path))
            msg.attach(attachment)
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_email, msg.as_string())

    except Exception as e:
        print(f'Error sending email: {e}')


        
@dp.message(F.text == '/start')
async def cmd_start(message: Message, state : StatesGroup):
    first_name = message.from_user.first_name

    await message.answer(f'Hi, *{first_name}*! How are you doing today?\nAre you ...?', parse_mode='Markdown', reply_markup=kb.cmd_start_kb)

@dp.callback_query(F.data =='main_menu')
async def open_main_menu(callback_query: types.CallbackQuery, state : StatesGroup):
    await state.update_data(None)
    await state.clear()
    await callback_query.message.edit_text(f'Select one of the items below 👇', parse_mode='Markdown', reply_markup=kb.cmd_start_kb)

@dp.callback_query(F.data =='existing_client')
async def existing_client(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Are you interested in?', reply_markup=kb.Existing_Client_kb)

@dp.callback_query(F.data =='new_client')
async def new_client(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Which service are you interested in?', reply_markup=kb.New_Client_kb)

@dp.message(Form.ExistingClientInfo)
async def Existing_Client_process_contact(message: types.Message, state: FSMContext):
    await message.answer('Your request has been successfully received', parse_mode='Markdown')
    await state.update_data(ExistingClientInfo=message.text)

    data_customer_response = await state.get_data()
    customer_response = data_customer_response.get('customer_response')

    data_Interested = await state.get_data()
    Interested = data_Interested.get('Interested')

    data = await state.get_data()
    user_info = data.get('ExistingClientInfo')

    user_username = message.from_user.username

    data = await state.get_data()
    screenshot_data = data.get('screenshot_data')

    text = f"EXISTING CLIENT\nInterested service: {Interested}\n{line}\nCustomer response: {customer_response}\n{line}\nContact: {user_info}\n{line}\nTelegram: @{user_username}"

    if screenshot_data:
        await send_email('EXISTING CLIENT', text, Recipient, screenshot_data)
        os.remove(screenshot_data)
    else:
        await send_email('EXISTING CLIENT', text, Recipient)

    await state.update_data(None)
    await state.clear()

@dp.message(Form.screenshot)
async def process_screenshot(message: types.Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id

        user_id = message.from_user.id

        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        file_url = f"https://api.telegram.org/file/bot{cfg.BOT_TOKEN}/{file_path}"

        project_folder = os.getcwd()

        save_dir = os.path.join(project_folder, 'downloaded_files')

        os.makedirs(save_dir, exist_ok=True)

        filename = os.path.join(save_dir, f"{user_id}_{file_path.split('/')[-1]}")
        await state.update_data(screenshot_data=filename)

        urllib.request.urlretrieve(file_url, filename)
    elif message.document:
        file_id = message.document.file_id

        user_id = message.from_user.id

        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        file_url = f"https://api.telegram.org/file/bot{cfg.BOT_TOKEN}/{file_path}"

        project_folder = os.getcwd()

        save_dir = os.path.join(project_folder, 'downloaded_files')

        os.makedirs(save_dir, exist_ok=True)

        filename = os.path.join(save_dir, f"{user_id}_{file_path.split('/')[-1]}")
        await state.update_data(screenshot_data=filename)

        urllib.request.urlretrieve(file_url, filename)

    else:
        await state.update_data(screenshot=None)

    await message.answer("Please leave your contact details.")
    await state.set_state(Form.ExistingClientInfo)  

@dp.message(Form.customer_response)
async def process_customer_response(message: types.Message, state: FSMContext):
    await state.update_data(customer_response=message.text)
    await message.answer("Do you have a file or screenshot?")
     
    await state.set_state(Form.screenshot)

@dp.callback_query(F.data =='service')
async def Chosen_Service(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="Service")

    await callback_query.message.edit_text(f'How can we help?', parse_mode='Markdown')
    await state.set_state(Form.customer_response)

@dp.callback_query(F.data =='accounting')
async def Chosen_Accounting(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="Accounting")

    await callback_query.message.edit_text(f'How can we help?', parse_mode='Markdown')
    await state.set_state(Form.customer_response)

@dp.callback_query(F.data =='it')
async def Chosen_IT(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="IT")

    await callback_query.message.edit_text('💵 What is the size of your budget?', reply_markup=kb.Budget_kb)

@dp.callback_query(F.data =='vop')
async def Chosen_VOP(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="VOP")

    await callback_query.message.edit_text('💵 What is the size of your budget?', reply_markup=kb.Budget_kb)

@dp.callback_query(F.data =='management_consultancy')
async def Chosen_Management_Consultancy(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="Management consultancy")

    await callback_query.message.edit_text('💵 What is the size of your budget?', reply_markup=kb.Budget_kb)

@dp.callback_query(F.data =='marketing')
async def Chosen_Marketing(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.Interested)
    await state.update_data(Interested="Marketing")

    await callback_query.message.edit_text('💵 What is the size of your budget?', reply_markup=kb.Budget_kb)


@dp.message(Form.NewUserContact)
async def New_User_process_contact(message: types.Message, state: FSMContext):
    await message.answer('Your request has been successfully received', parse_mode='Markdown')


    await state.update_data(UserContact=message.text)

    data_Interested = await state.get_data()
    Interested = data_Interested.get('Interested')

    data_budget = await state.get_data()
    Budget = data_budget.get('Budget')

    data = await state.get_data()
    user_contact = data.get('UserContact')

    user_username = message.from_user.username

    text = f"NEW CLIENT\nInterested service: {Interested}\n{line}\nBudget: {Budget}\n{line}\nContact: {user_contact}\n{line}\nTelegram: @{user_username}"

    await send_email('New Client', text, Recipient)

    await state.update_data(None)
    await state.clear()

@dp.callback_query(F.data =='zero-ten')
async def Chosen_Budget_zero_ten(callback_query: types.CallbackQuery, state : StatesGroup):
    await state.set_state(Form.Budget)
    await state.update_data(Budget="0-10k")

    await callback_query.message.edit_text('Please leave your contact info, and we will contact you as soon it possible')
    await state.set_state(Form.NewUserContact)


@dp.callback_query(F.data =='ten-hundred')
async def Chosen_Budget_ten_hundred(callback_query: types.CallbackQuery, state : StatesGroup):
    await state.set_state(Form.Budget)
    await state.update_data(Budget="10-100k")

    await callback_query.message.edit_text('Please leave your contact info, and we will contact you as soon it possible')
    await state.set_state(Form.NewUserContact)

@dp.callback_query(F.data =='hundred+')
async def Chosen_Budget_hundred(callback_query: types.CallbackQuery, state : StatesGroup):
    await state.set_state(Form.Budget)
    await state.update_data(Budget="100k +")

    await callback_query.message.edit_text('Please leave your contact info, and we will contact you as soon it possible')
    await state.set_state(Form.NewUserContact)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())