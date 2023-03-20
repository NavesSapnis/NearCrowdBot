import parseMoney
import AllPrice
from states import *
from time import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from string import *
import emoji
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from db import BotDB
import parseMoney


BotDB = BotDB('users.db')

logging.basicConfig(level=logging.INFO)
bot = Bot(token='5621098161:AAEFBJpk6Au5owGw0sd9id9bb8JMsxDCUko')#token here
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def get_info(acc, pr):
    return parseMoney.get_money(acc, pr)


def start_buttons():
    button1 = KeyboardButton('добавить новый аккаунт' +
                             emoji.emojize(":star_of_David:"))
    button2 = KeyboardButton('мои аккаунты'+emoji.emojize(":star:"))
    button3 = KeyboardButton('цены на криптовалюты'+emoji.emojize(":eyes:"))
    button4 = KeyboardButton('добавить новый аккаунт рабочего')
    button5 = KeyboardButton('аккаунты моих рабочих')
    button6 = KeyboardButton('удалить аккаунт из списка')
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup1.row(button1, button2, button3, button4, button5, button6)
    return markup1


@dp.message_handler(state=crypto_st.crypto)
async def cypto(message: types.Message, state: FSMContext):
    if message.text == 'вернуться'+emoji.emojize(":door:"):
        await message.answer("Сейчас вы находитесь в главном меню\n", reply_markup=start_buttons())
        await state.finish()
    else:
        try:
            await message.answer(AllPrice.GetPrice(message.text.upper()))
        except:
            await message.answer("Простите, такой торговой пары нет, торговые пары выглядят так BTCUSDT")


@dp.message_handler(state=add_acc_st.add_new_acc_step5)
async def newacc(message: types.Message, state: FSMContext):
    global keys, worker_acc
    keys = message.text
    BotDB.add_worker_acc(message.from_user.id, name,
                         procent, personal_name, wallet, keys)
    await message.answer("Аккаунт добавлен\n")
    worker_acc = False
    await state.finish()


@dp.message_handler(state=add_acc_st.add_new_acc_step4)
async def newacc(message: types.Message, state: FSMContext):
    global wallet, worker_acc
    wallet = message.text
    await message.answer("Напишите ваш приватный ключ от кошелька\n")
    await state.finish()
    await add_acc_st.add_new_acc_step5.set()


@dp.message_handler(state=add_acc_st.add_new_acc_step3)
async def newacc(message: types.Message, state: FSMContext):
    global personal_name, worker_acc
    personal_name = message.text
    personal_name = personal_name.replace(' ', '_')
    text = ""
    if (worker_acc == False):
        if (not BotDB.name_check(personal_name)):
            BotDB.add_my_acc(message.from_user.id, name,
                             procent, personal_name)
            text = "аккаунт добавлен"
            await state.finish()
        else:
            await state.finish()
            text = "аккаунт с таким именем существует, повторите попытку"

    else:
        if (not BotDB.name_check2(personal_name)):
            text = "пришлите кошелек рабочего"
            await add_acc_st.add_new_acc_step4.set()
        else:
            await state.finish()
            text = "аккаунт с таким именем существует, повторите попытку"
            worker_acc = False

    await message.answer(text, reply_markup=start_buttons())


@dp.message_handler(state=add_acc_st.add_new_acc_step2)
async def newacc(message: types.Message, state: FSMContext):
    global procent, worker_acc
    procent = 1
    procent = message.text
    try:
        procent = int(procent)
    except:
        await state.finish()
        await message.answer("Некорректное кол-во процентов. Процент это целое число, в диапазоне от 1 до 100, повторите попытку\n", reply_markup=start_buttons())
        worker_acc = False

    if (type(int(procent)) == int and int(procent) < 100 and int(procent) > 1):
        await message.answer("придумайте название аккаунта\n")
        await state.finish()
        await add_acc_st.add_new_acc_step3.set()
    else:
        await state.finish()
        await message.answer("Некорректное кол-во процентов. Процент это целое число, в диапазоне от 1 до 100, повторите попытку\n", reply_markup=start_buttons())
        worker_acc = False


@dp.message_handler(state=add_acc_st.add_new_acc_step1)
async def newacc(message: types.Message, state: FSMContext):
    global name
    name = message.text
    await message.answer("Хорошо, теперь напишите получамый процент\n")
    await state.finish()
    await add_acc_st.add_new_acc_step2.set()


@dp.message_handler(state=get_acc_st.my_acc_step1)
async def myacc(message: types.Message, state: FSMContext):
    if message.text == 'вернуться'+emoji.emojize(":door:"):
        await message.answer("Сейчас вы находитесь в главном меню\n", reply_markup=start_buttons())
        await state.finish()
    elif (message.text == "Показать всё бабло" + emoji.emojize(":money_with_wings:")):
        try:
            summ = 0
            mes = await message.answer("Придётся немного подождать, этот бот использует секретные разработки китайских программистов, которые долго исполняются на сервере ")
            for i in range(int(f"{len(BotDB.get_my_acc(message.from_user.id))}")):
                a = f"{BotDB.get_my_acc(message.from_user.id)[i]}"
                a = a[:-3]
                a = a[2:]

                b = f"{BotDB.get_procent(a, message.from_user.id)}"
                a = f"{BotDB.get_acc(a, message.from_user.id)}"
                while a == "" or b =="":
                    try:
                        b = f"{BotDB.get_procent(a, message.from_user.id)}"
                        a = f"{BotDB.get_acc(a, message.from_user.id)}"
                    except:
                        await message.answer("Сервера в ужасном состоянии, загрузка будет дольше")
                        sleep(4)
                a = a[:-3]
                a = a[2:]

                b = b[:-2]
                b = b[1:]

                summ += get_info(str(a), int(b))
            dollars = AllPrice.get_price_wd("NEARUSDT") * float(summ)
            await message.answer(str(summ) + " Ⓝ\n" + str(dollars) + " $")
        except:
            await message.answer("Не получилось получить данные по аккаунтам, проверьте правильность данных")
    else:
        info = ""
        try:
            a = BotDB.get_acc(message.text, message.from_user.id)
            a = f"{a[0]}"
            b = BotDB.get_procent(message.text, message.from_user.id)
            b = f"{b[0]}"
            while info == "":
                try:
                    info = get_info(str(a), int(b))
                except:
                    await message.answer("Сервера в ужасном состоянии, загрузка будет дольше")
                    sleep(4)
            await message.answer("Вам должны выплатить с этого аккаунта "+str(info) + " Ⓝ")
        except:
            print("Инфо" + info)
            await message.answer("Не получилось получить данные по аккаунту, проверьте правильность данных")


@dp.message_handler(state=get_acc_st.worker_acc_step1)
async def myacc(message: types.Message, state: FSMContext):
    if message.text == 'вернуться'+emoji.emojize(":door:"):
        await message.answer("Сейчас вы находитесь в главном меню\n", reply_markup=start_buttons())
        await state.finish()
    else:
        info = ""
        try:
            a = BotDB.get_acc2(message.text, message.from_user.id)
            a = f"{a[0]}"
            b = BotDB.get_procent2(message.text, message.from_user.id)
            b = f"{b[0]}"
            while info == "":
                try:
                    info = get_info(str(a), int(b))
                except:
                    await message.answer("Сервера в ужасном состоянии, загрузка будет дольше")
                    sleep(4)

            await message.answer("Вам должны выплатить с этого аккаунта "+str(info) + " Ⓝ")
        except:
            print("Инфо" + info)
            await message.answer("Не получилось получить данные по аккаунту, проверьте правильность данных")


@dp.message_handler(state=delete_acc_st.delete_acc_step1)
async def myacc(message: types.Message, state: FSMContext):
    delete_acc = message.text
    if message.text == 'вернуться'+emoji.emojize(":door:"):
        await message.answer("Сейчас вы находитесь в главном меню\n", reply_markup=start_buttons())
        await state.finish()
    else:
        try:
            BotDB.remove_my_acc(message.from_user.id, delete_acc)
            await message.answer("Аккаунт удален")
        except:
            await message.answer("Аккаунт не найден")


global worker_acc
worker_acc = False


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.lower() == 'start' or message.text.lower() == '/start':
        if (not BotDB.user_exists(message.from_user.id)):
            BotDB.add_user(message.from_user.id)

        await message.answer("Сейчас вы находитесь в главном меню\n", reply_markup=start_buttons())

    elif message.text.lower() == 'добавить новый аккаунт'+emoji.emojize(":star_of_David:"):
        await message.answer("Пришли мне кошелек аккаунта, он может заканчивется на .near\n")
        await add_acc_st.add_new_acc_step1.set()

    elif message.text.lower() == 'добавить новый аккаунт рабочего':
        global worker_acc
        worker_acc = True
        await message.answer("Пришли мне кошелек аккаунта, он может заканчивется на .near\n")
        await add_acc_st.add_new_acc_step1.set()

    elif message.text.lower() == 'удалить аккаунт из списка':
        button1 = KeyboardButton('вернуться'+emoji.emojize(":door:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        accounts = BotDB.get_my_acc(message.from_user.id)
        res = "Ваши аккаунты:\n"
        for i in range(len(accounts)):
            res += f"- {accounts[i][0]}\n"
            tempRes = f"{accounts[i][0]}\n"
            temp = KeyboardButton(tempRes)
            buttons.append(temp)

        markup1.row(button1)
        for i in range(len(buttons)):
            markup1.add(buttons[i])

        await message.answer(res, reply_markup=markup1)
        await delete_acc_st.delete_acc_step1.set()

    elif message.text.lower() == 'мои аккаунты'+emoji.emojize(":star:"):
        button1 = KeyboardButton('вернуться'+emoji.emojize(":door:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        accounts = BotDB.get_my_acc(message.from_user.id)
        res = "Ваши аккаунты:\n"
        for i in range(len(accounts)):
            res += f"- {accounts[i][0]}\n"
            tempRes = f"{accounts[i][0]}\n"
            temp = KeyboardButton(tempRes)
            buttons.append(temp)
        buttons.append("Показать всё бабло" + emoji.emojize(":money_with_wings:"))

        markup1.row(button1)
        for i in range(len(buttons)):
            markup1.row(buttons[i])

        await message.answer(res, reply_markup=markup1)
        await get_acc_st.my_acc_step1.set()

    elif message.text.lower() == 'аккаунты моих рабочих':
        button1 = KeyboardButton('вернуться'+emoji.emojize(":door:"))
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        accounts = BotDB.get_worker_acc(message.from_user.id)
        res = "Ваши аккаунты:\n"
        for i in range(len(accounts)):
            res += f"- {accounts[i][0]}\n"
            tempRes = f"{accounts[i][0]}\n"
            temp = KeyboardButton(tempRes)
            buttons.append(temp)

        markup1.row(button1)
        for i in range(len(buttons)):
            markup1.add(buttons[i])

        await message.answer(res, reply_markup=markup1)
        await get_acc_st.worker_acc_step1.set()

    elif message.text.lower() == 'цены на криптовалюты'+emoji.emojize(":eyes:"):
        button1 = KeyboardButton('вернуться'+emoji.emojize(":door:"))
        button2 = KeyboardButton('BTCUSDT')
        button3 = KeyboardButton('ETHUSDT')
        button4 = KeyboardButton('NEARUSDT')
        button5 = KeyboardButton('XRPUSDT')
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(button3, button2, button1, button4, button5)
        await message.answer("Напишите торговую пару, которую хотите просмотреть\n", reply_markup=markup1)
        await crypto_st.crypto.set()

    elif message.text.lower() == '/help' or message.text.lower() == 'help':
        await bot.send_message(message.chat.id, """Доброго времени суток!\nМеня зовут Дося, я создан, чтобы упростить работу пользователя в NearCrowd.\n Пожалуйста используйте кпопочки ниже, которые помогут вам ориентироваться.""")

    else:
        await bot.send_message(message.chat.id, """Не разумею вас напишите /start""")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
