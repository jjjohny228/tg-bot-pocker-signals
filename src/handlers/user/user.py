import asyncio
import datetime
import random
from functools import wraps

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from config import Config
from src.create_bot import bot
from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
from src.utils import send_typing_action, logger
from src.database.user import (create_user_if_not_exist, check_has_user_pocket_id_and_deposit,
    check_pocket_id, set_pocket_id, set_pocket_deposit, set_user_pocket_id,
    check_user_deposit)
from src.handlers.user.messages import Messages
from src.handlers.user.kb import Keyboards
from src.misc import SignalStates, UserDataInputting


def delete_callback_message(func):
    @wraps(func)  # Сохраняем метаданные оригинальной функции
    async def wrapper(*args, **kwargs):
        callback = args[0]  # Получаем объект CallbackQuery
        try:
            await callback.message.delete()
        except exceptions.MessageCantBeDeleted:
            logger.error('Сообщение устарело и не может быть удалено')
        except Exception as e:
            logger.error(f'Ошибка при удалении сообщения: {e}')

        return await func(*args, **kwargs)  # ✅ Добавляем `await` для вызова асинхронной функции

    return wrapper


async def __handle_start_command(message: Message, state: FSMContext) -> None:
    await state.finish()
    if await check_is_admin(message):
        await send_admin_menu(message)
    else:
        await send_typing_action(message)

        user = create_user_if_not_exist(
            telegram_id=message.from_id,
            name=message.from_user.username or message.from_user.full_name,
            reflink=message.get_full_command()[1]
        )

        if check_has_user_pocket_id_and_deposit(user):
            await message.answer_photo(
                photo=Messages.get_signals_menu_photo(),
                caption=Messages.get_signals_menu_message(),
                reply_markup=Keyboards.get_signals_menu()
            )
        else:
            await message.answer_photo(
                photo=Messages.get_welcome_photo(),
                caption=Messages.get_welcome_message(message),
                reply_markup=Keyboards.get_welcome_menu()
            )

@delete_callback_message
async def __handle_authenticated_start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.finish()

    await callback.message.answer_photo(
        photo=Messages.get_signals_menu_photo(),
        caption=Messages.get_signals_menu_message(),
        reply_markup=Keyboards.get_signals_menu()
    )

@delete_callback_message
async def __handle_unauthenticated_start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.finish()

    await callback.message.answer_photo(
        photo=Messages.get_welcome_photo(),
        caption=Messages.get_welcome_message(callback.message),
        reply_markup=Keyboards.get_welcome_menu()
    )


async def __handle_new_registered_mammoth(message: Message) -> None:
    pocket_id = int(message.text.split('_')[1])
    admin_ids = Config.ADMIN_IDS
    if not check_pocket_id(pocket_id):
        set_pocket_id(pocket_id)
        for user_id in admin_ids:
            try:
                await bot.send_message(chat_id=user_id, text=f'Зарегистрировался новый пользователь с id: {pocket_id}')
            except (ChatNotFound, BotBlocked):
                logger.error(f'Пользователь не запустил бота или заблокировал его.')
            await asyncio.sleep(0.05)
        logger.info(f'Рассылка закончилась.')


async def __handle_new_deposit(message: Message) -> None:
    _, pocket_id, amount = message.text.split('_')
    admin_ids = Config.ADMIN_IDS
    set_pocket_deposit(pocket_id)
    for user_id in admin_ids:
        try:
            await bot.send_message(chat_id=user_id, text=f'Польователь с id {pocket_id} оформил депозит {amount}')
        except (ChatNotFound, BotBlocked):
            logger.error(f'Админ не запустил бота или заблокировал его.')
        await asyncio.sleep(0.05)
    logger.info(f'Рассылка закончилась.')


@delete_callback_message
async def __handle_registration_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(
        caption=Messages.get_registration_message(),
        photo=Messages.get_registration_photo(),
        reply_markup=Keyboards.get_registration_menu()
    )


@delete_callback_message
async def __handle_check_registration_callback(callback: CallbackQuery):
    await callback.message.answer(
        text=Messages.get_ask_for_pocket_id_message()
    )
    await UserDataInputting.wait_for_id.set()


async def __handle_user_id_message(message: Message, state: FSMContext):
    await send_typing_action(message)

    if not message.text.isdigit() or len(message.text) not in (8, 9):
        await message.answer(Messages.get_bullshit_registration_message())
        return
    print(message.text)
    if check_pocket_id(int(message.text)):
        set_user_pocket_id(message.from_user.id, message.text)
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=Messages.get_deposit_photo(),
                             caption=Messages.get_deposit_message(),
                             reply_markup=Keyboards.get_deposit_markup())
        await state.finish()

    else:
        await message.answer_photo(
            caption=Messages.get_registration_fail_message(),
            photo=Messages.get_invalid_registration_photo(),
            reply_markup=Keyboards.get_registration_menu()
        )
        await state.finish()
        return


@delete_callback_message
async def __handle_check_deposit_callback(callback: CallbackQuery, state: FSMContext):
    if check_user_deposit(callback.message.chat.id):
        await callback.message.answer(text=Messages.get_successful_deposit_text())
        await callback.message.answer_photo(
            photo=Messages.get_signals_menu_photo(),
            caption=Messages.get_signals_menu_message(),
            reply_markup=Keyboards.get_signals_menu()
        )

    else:
        await callback.message.answer_photo(
            photo=Messages.get_deposit_photo(),
            caption=Messages.get_invalid_deposit_message(),
            reply_markup=Keyboards.get_deposit_markup()
        )
    await callback.answer()

@delete_callback_message
async def __handle_benefit_callback(callback: CallbackQuery) -> None:
    await callback.message.answer_photo(photo=Messages.get_benefit_photo(),
                                        caption=Messages.get_benefit_message(),
                                        reply_markup=Keyboards.get_back_main_button())
    await callback.answer()

@delete_callback_message
async def __handle_signals_menu_callback(callback: CallbackQuery):
    await callback.message.answer_photo(photo=Messages.get_signals_menu_photo(),
                                        caption=Messages.get_signals_menu_message(),
                                        reply_markup=Keyboards.get_signals_menu())
    await callback.answer()

@delete_callback_message
async def __handle_currency_signal_callback(callback: CallbackQuery):
    signal_type = callback.data.split('_')[0]
    await callback.message.answer_photo(photo=Messages.get_currency_pairs_photo(signal_type),
                                        caption=Messages.get_currency_pairs_message(signal_type),
                                        reply_markup=Keyboards.get_signal_pairs_menu(signal_type))
    await SignalStates.pair.set()
    await callback.answer()

@delete_callback_message
async def __handle_pair_choice_callback(callback: CallbackQuery, state: FSMContext):
    signal_text = callback.data.split('_')[1]
    async with state.proxy() as data:
        data["pair"] = signal_text
    await callback.message.answer(text=Messages.get_analysis_type_message(),
                                  reply_markup=Keyboards.get_analysis_menu())
    await SignalStates.global_analysis_type.set()
    await callback.answer()

@delete_callback_message
async def __handle_global_analysis_type_choice_callback(callback: CallbackQuery, state: FSMContext):
    analysis_type = callback.data.split('_')[0]
    async with state.proxy() as data:
        data["global_analysis_type"] = analysis_type
    if analysis_type == 'indicator':
        await callback.message.answer(text=Messages.get_indicator_analysis_message(),
                                      reply_markup=Keyboards.get_indicator_analysis_menu())
    elif analysis_type == 'candle':
        await callback.message.answer(text=Messages.get_candle_analysis_message(),
                                  reply_markup=Keyboards.get_candle_analysis_menu())
    await SignalStates.analysis_type.set()
    await callback.answer()


@delete_callback_message
async def __handle_analysis_type_choice_callback(callback: CallbackQuery, state: FSMContext):
    analysis_type = callback.data.split('_')[0]
    async with state.proxy() as data:
        data["analysis_type"] = analysis_type

    await callback.message.answer_photo(photo=Messages.get_trade_time_photo(),
                                        caption=Messages.get_trade_time_message(),
                                        reply_markup=Keyboards.get_time_menu())
    await SignalStates.trade_time.set()
    await callback.answer()

@delete_callback_message
async def __handle_time_choice_callback(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split('_')[0]
    async with state.proxy() as data:
        data["trade_time"] = time

    # Send signal
    await send_signal(callback.message, data['pair'], data["trade_time"],
                      data['global_analysis_type'], data['analysis_type'])
    await state.finish()
    await callback.answer()

async def send_signal(message, pair_text, trade_time, global_analysis_type, analysis_type):
    trade_moves = ('Buy', 'Sell')
    trade_move = random.choice(trade_moves)
    current_time = f'{datetime.datetime.now().strftime("%H:%M")} UTC'
    msg = await message.answer(text='📊')
    msg_analysis = await message.answer(f'⚠️ Doing market analysis ~ 3')
    await asyncio.sleep(1)
    for second in (2, 1):
        await msg_analysis.edit_text(f'⚠️ Doing market analysis ~ {second}')
        await asyncio.sleep(1)
    await msg_analysis.delete()
    await msg.delete()
    await message.answer_photo(photo=Messages.get_signal_photo(trade_move),
                               caption=Messages.get_signal_message(pair_text, trade_time, current_time,
                                                                   global_analysis_type, analysis_type, trade_move),
                               reply_markup=Keyboards.get_signal_menu())

async def __change_signal_page(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    signal_type = callback_query.data.split("_")[2]
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.get_signal_pairs_menu(signal_type, page))
    await callback_query.answer()

async def __change_indicator_page(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[2])
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.get_indicator_analysis_menu(page))
    await callback_query.answer()



def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(__handle_start_command, commands='start', state='*')
    dp.register_callback_query_handler(__change_signal_page, lambda c: c.data.startswith("page_"), state='*')
    dp.register_callback_query_handler(__change_indicator_page, lambda c: c.data.startswith("indicator_page"), state='*')
    dp.register_callback_query_handler(__handle_authenticated_start_callback, text='start_callback', state='*')
    dp.register_callback_query_handler(__handle_unauthenticated_start_callback, text='unauthenticated_start_callback', state='*')
    dp.register_callback_query_handler(__handle_benefit_callback, text='user_benefits')

    dp.register_callback_query_handler(__handle_check_deposit_callback, text='check_deposit', state=None)
    dp.register_callback_query_handler(__handle_registration_menu_callback, text='registration_request', state=None)
    dp.register_callback_query_handler(__handle_check_registration_callback, text='check_registration', state=None)
    dp.register_message_handler(__handle_user_id_message, state=UserDataInputting.wait_for_id)
    dp.register_channel_post_handler(__handle_new_registered_mammoth, lambda text: text.text.startswith("registered"))
    dp.register_channel_post_handler(__handle_new_deposit, lambda text: text.text.startswith("deposit"))

    dp.register_callback_query_handler(__handle_signals_menu_callback, text='get_signals')
    dp.register_callback_query_handler(__handle_currency_signal_callback, lambda c: c.data.endswith("signal"))
    dp.register_callback_query_handler(__handle_pair_choice_callback, lambda c: c.data.startswith("pair"), state=SignalStates.pair)
    dp.register_callback_query_handler(__handle_global_analysis_type_choice_callback, lambda c: c.data.endswith("analysis"), state=SignalStates.global_analysis_type)
    dp.register_callback_query_handler(__handle_analysis_type_choice_callback,
                                       lambda c: c.data.endswith("analysis_type"), state=SignalStates.analysis_type)
    dp.register_callback_query_handler(__handle_time_choice_callback,
                                       lambda c: c.data.endswith("time"), state=SignalStates.trade_time)