from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions

from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
from src.utils import send_typing_action, logger
from src.database.user import create_user_if_not_exist, check_has_user_pocket_id_and_deposit
from src.handlers.user.messages import Messages
from src.handlers.user.kb import Keyboards


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

async def __handle_pair_choice_callback(callback: CallbackQuery, state: FSMContext):
    # прописать что пара записывается в state data
    print(callback.data)
    await callback.message.answer(text=Messages.get_analysis_type_message(),
                                  reply_markup=Keyboards.get_analysis_menu())

async def change_page(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    signal_type = callback_query.data.split("_")[2]
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.get_signal_pairs_menu(signal_type, page))



def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(__handle_start_command, commands='start')
    dp.register_callback_query_handler(change_page, lambda c: c.data.startswith("page_"))
    dp.register_callback_query_handler(__handle_start_callback, text='start_callback')
    dp.register_callback_query_handler(__handle_signals_menu_callback, text='get_signals')
    dp.register_callback_query_handler(__handle_currency_signal_callback, lambda c: c.data.endswith("signal"))
    dp.register_callback_query_handler(__handle_pair_choice_callback, lambda c: c.data.startswith("pair"))