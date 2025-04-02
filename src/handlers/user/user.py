import datetime
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions

from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
from src.utils import send_typing_action, logger
from src.database.user import create_user_if_not_exist, check_has_user_pocket_id_and_deposit
from src.handlers.user.messages import Messages
from src.handlers.user.kb import Keyboards
from src.misc import SignalStates


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


async def __handle_start_callback(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except exceptions.MessageCantBeDeleted:
        logger.error(f'Сообщение устарело и не может быть удалено')
    finally:
        await send_typing_action(callback.message)

        user = create_user_if_not_exist(
            telegram_id=callback.message.from_id,
            name=callback.message.from_user.username or callback.message.from_user.full_name,
            reflink=callback.message.get_full_command()[1]
        )

        if check_has_user_pocket_id_and_deposit(user):
            await callback.message.answer_photo(
                photo=Messages.get_signals_menu_photo(),
                caption=Messages.get_signals_menu_message(),
                reply_markup=Keyboards.get_signals_menu()
            )
        else:
            await callback.message.answer_photo(
                photo=Messages.get_welcome_photo(),
                caption=Messages.get_welcome_message(callback.message),
                reply_markup=Keyboards.get_welcome_menu()
            )

async def __handle_signals_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(photo=Messages.get_signals_menu_photo(),
                                        caption=Messages.get_signals_menu_message(),
                                        reply_markup=Keyboards.get_signals_menu())

async def __handle_currency_signal_callback(callback: CallbackQuery, state: FSMContext):
    signal_type = callback.data.split('_')[0]
    await callback.message.answer_photo(photo=Messages.get_currency_pairs_photo(),
                                        caption=Messages.get_currency_pairs_message(),
                                        reply_markup=Keyboards.get_signal_pairs_menu(signal_type))
    await SignalStates.pair.set()

async def __handle_pair_choice_callback(callback: CallbackQuery, state: FSMContext):
    # прописать что пара записывается в state data
    signal_text = callback.data.split('_')[1]
    async with state.proxy() as data:
        data["pair"] = signal_text
    await callback.message.answer(text=Messages.get_analysis_type_message(),
                                  reply_markup=Keyboards.get_analysis_menu())
    await SignalStates.global_analysis_type.set()

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


async def __handle_analysis_type_choice_callback(callback: CallbackQuery, state: FSMContext):
    # прописать что пара записывается в state data
    analysis_type = callback.data.split('_')[0]
    async with state.proxy() as data:
        data["analysis_type"] = analysis_type

    await callback.message.answer_photo(photo=Messages.get_trade_time_photo(),
                                        caption=Messages.get_trade_time_message(),
                                        reply_markup=Keyboards.get_time_menu())
    await SignalStates.trade_time.set()

async def __handle_time_choice_callback(callback: CallbackQuery, state: FSMContext):
    # прописать что пара записывается в state data
    time = callback.data.split('_')[0]
    async with state.proxy() as data:
        data["trade_time"] = time

    # Send signal
    await send_signal(callback.message, data['pair'], data["trade_time"],
                      data['global_analysis_type'], data['analysis_type'])
    await state.finish()


async def send_signal(message, pair_text, trade_time, global_analysis_type, analysis_type):
    trade_moves = ('Buy', 'Sell')
    trade_move = random.choice(trade_moves)
    current_time = f'{datetime.datetime.now().strftime("%H:%M")} UTC'
    await message.answer_photo(photo=Messages.get_signal_photo(trade_move),
                               caption=Messages.get_signal_message(pair_text, trade_time, current_time,
                                                                   global_analysis_type, analysis_type, trade_move),
                               reply_markup=Keyboards.get_signal_menu())

async def __change_signal_page(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    signal_type = callback_query.data.split("_")[2]
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.get_signal_pairs_menu(signal_type, page))

async def __change_indicator_page(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[2])
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.get_indicator_analysis_menu(page))



def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(__handle_start_command, commands='start')
    dp.register_callback_query_handler(__change_signal_page, lambda c: c.data.startswith("page_"), state='*')
    dp.register_callback_query_handler(__change_indicator_page, lambda c: c.data.startswith("indicator_page"), state='*')
    dp.register_callback_query_handler(__handle_start_callback, text='start_callback')
    dp.register_callback_query_handler(__handle_signals_menu_callback, text='get_signals')
    dp.register_callback_query_handler(__handle_currency_signal_callback, lambda c: c.data.endswith("signal"))
    dp.register_callback_query_handler(__handle_pair_choice_callback, lambda c: c.data.startswith("pair"), state=SignalStates.pair)
    dp.register_callback_query_handler(__handle_global_analysis_type_choice_callback, lambda c: c.data.endswith("analysis"), state=SignalStates.global_analysis_type)
    dp.register_callback_query_handler(__handle_analysis_type_choice_callback,
                                       lambda c: c.data.endswith("analysis_type"), state=SignalStates.analysis_type)
    dp.register_callback_query_handler(__handle_time_choice_callback,
                                       lambda c: c.data.endswith("time"), state=SignalStates.trade_time)