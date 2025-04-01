import os
from venv import logger

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.utils import logger




class Keyboards:
    PAIRS_PER_PAGE = 6
    currency_pairs = (
    "🇦🇺 AUD/CAD OTC 🇨🇦", "🇦🇺 AUD/CHF OTC 🇨🇭", "🇦🇺 AUD/USD OTC 🇺🇸",
    "🇨🇦 CAD/CHF OTC 🇨🇭", "🇨🇦 CAD/JPY OTC 🇯🇵", "🇨🇭 CHF/NOK OTC 🇳🇴",
    "🇪🇺 EUR/CHF OTC 🇨🇭", "🇪🇺 EUR/GBP OTC 🇬🇧", "🇪🇺 EUR/JPY OTC 🇯🇵",
    "🇪🇺 EUR/NZD OTC 🇳🇿", "🇪🇺 EUR/TRY OTC 🇹🇷", "🇪🇺 EUR/USD OTC 🇺🇸",
    "🇬🇧 GBP/JPY OTC 🇯🇵", "🇳🇿 NZD/JPY OTC 🇯🇵", "🇺🇸 USD/BDT OTC 🇧🇩",
    "🇺🇸 USD/BRL OTC 🇧🇷", "🇺🇸 USD/BRL OTC 🇧🇷", "🇺🇸 USD/JPY OTC 🇯🇵",
    "🇺🇸 USD/RUB OTC 🇷🇺", "🇺🇸 USD/SGD OTC 🇸🇬", "🇺🇸 USD/THB OTC 🇹🇭",
    "🇺🇸 USD/EGP OTC 🇪🇬", "🇨🇭 CHF/JPY OTC 🇯🇵", "🇺🇸 USD/CHF OTC 🇨🇭",
    "🇺🇸 USD/INR OTC 🇮🇳", "🇳🇿 NZD/USD OTC 🇺🇸", "🇺🇸 USD/IDR OTC 🇮🇩",
    "🇦🇺 AUD/JPY OTC 🇯🇵", "🇪🇺 EUR/RUB OTC 🇷🇺", "🇺🇸 USD/MXN OTC 🇲🇽",
    "🇺🇸 USD/CNH OTC 🇨🇳", "🇦🇺 AUD/NZD OTC 🇳🇿", "🇺🇸 USD/MYR OTC 🇲🇾",
    "🇺🇸 USD/PKR OTC 🇵🇰", "🇺🇸 USD/DZD OTC 🇩🇿", "🇺🇸 USD/ARS OTC 🇦🇷",
    "🇪🇺 EUR/HUF OTC 🇭🇺", "🇺🇸 USD/VND OTC 🇻🇳", "🇬🇧 GBP/AUD OTC 🇦🇺",
    "🇺🇸 USD/PHP OTC 🇵🇭", "🇺🇸 USD/CLP OTC 🇨🇱", "🇺🇸 USD/COP OTC 🇨🇴"
)

    all_pairs = {
        'currency': currency_pairs,
    }
    @staticmethod
    def get_welcome_menu() -> InlineKeyboardMarkup:
        activate_button = InlineKeyboardButton('🚀Activate bot🚀', callback_data='registration_request')
        benefit_button = InlineKeyboardButton("❔️What I'm getting❔️", callback_data='user_benefits')
        channel_button = InlineKeyboardButton('💰Telegram channel💰', url='https://www.google.com/')
        questions_pirates_button = InlineKeyboardButton('⁉️Any questions ⁉️️', url='https://www.google.com/')
        instruction_button = InlineKeyboardButton('📖Instruction📖', url='https://www.google.com/')
        feedback_button = InlineKeyboardButton('👥Feedback👥', url='https://www.google.com/')
        return InlineKeyboardMarkup(row_width=1).add(activate_button, benefit_button, channel_button,
                                                     questions_pirates_button, instruction_button, feedback_button)

    @staticmethod
    def get_registration_menu(menu_owner: str) -> InlineKeyboardMarkup:
        registration_button = InlineKeyboardButton('🔗Registration link', url=os.getenv('REF_URL', 'Впишите реферальную ссылку'))
        check_registration_button = InlineKeyboardButton('🔎Check Registration', callback_data='check_registration')
        back_button = InlineKeyboardButton('🔙Back', callback_data=f'start_callback')
        return InlineKeyboardMarkup(row_width=1).add(registration_button, check_registration_button, back_button)

    @staticmethod
    def get_back_registration_button(menu_owner: str) -> InlineKeyboardMarkup:
        menu_button = InlineKeyboardButton('🔙Back', callback_data=f'registration_request')
        return InlineKeyboardMarkup(row_width=1).add(menu_button)

    @staticmethod
    def get_deposit_markup() -> InlineKeyboardMarkup:
        deposit_button = InlineKeyboardButton('💰Top up💰', url=os.getenv('DEP_URL'))
        deposit_check_button = InlineKeyboardButton('Check deposit ✅', callback_data='check_deposit')
        return InlineKeyboardMarkup(row_width=1).add(deposit_button, deposit_check_button)

    # @staticmethod
    # def get_main_menu() -> InlineKeyboardMarkup:
    #     signals_button = InlineKeyboardButton('⚡️Get signal', callback_data='get_signals')
    #     return InlineKeyboardMarkup(row_width=1).add(signals_button)

    @staticmethod
    def get_signals_menu() -> InlineKeyboardMarkup:
        currency_signal_button = InlineKeyboardButton('💹Сurrency pairs', callback_data='currency_signal')
        cryptocurrency_signal_button = InlineKeyboardButton('💰Cryptocurrency', callback_data='cryptocurrency_signal')
        commodities_signal_button = InlineKeyboardButton('🏆Commodities', callback_data='commodities_signal')
        shares_signal_button = InlineKeyboardButton('📈Shares', callback_data='shares_signal')
        indices_signal_button = InlineKeyboardButton('📊Indices', callback_data='indices_signal')
        # back_main_menu_button = InlineKeyboardButton('🔙Back', callback_data=f'main_menu')
        return InlineKeyboardMarkup(row_width=1).add(currency_signal_button, cryptocurrency_signal_button,
                                                     commodities_signal_button, shares_signal_button,
                                                     indices_signal_button)

    @classmethod
    def get_signal_pairs_menu(cls, signal_type: str, page: int = 0) -> InlineKeyboardMarkup | None:
        keyboard = InlineKeyboardMarkup(row_width=2)
        start_idx = page * cls.PAIRS_PER_PAGE
        end_idx = start_idx + cls.PAIRS_PER_PAGE
        keyboard_pairs = cls.all_pairs.get(signal_type)
        if not keyboard_pairs:
            logger.error("There is no such pair type in all_pairs")
            return
        current_pairs = keyboard_pairs[start_idx:end_idx]

        # Добавляем кнопки с валютными парами
        for pair in current_pairs:
            pair_text = pair[3:len(pair)-2]
            keyboard.insert(InlineKeyboardButton(text=pair, callback_data=f"pair_{pair_text}"))

        # Кнопки пагинации
        total_pages = (len(keyboard_pairs) - 1) // cls.PAIRS_PER_PAGE + 1
        pagination_buttons = []

        if page > 0:
            pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}_{signal_type}"))

        pagination_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none"))

        if end_idx < len(keyboard_pairs):
            pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}_{signal_type}"))

        keyboard.row(*pagination_buttons)

        # Кнопка "Назад"
        keyboard.add(InlineKeyboardButton(text="⬅ Назад", callback_data="get_signals"))

        return keyboard

    @staticmethod
    def get_analysis_menu():
        indicator_analysis_button = InlineKeyboardButton('🚀Indicator🚀', callback_data='currency_signal')
        candle_analysis_button = InlineKeyboardButton('🧨Candle🧨', callback_data='currency_signal')
        return InlineKeyboardMarkup(row_width=1).add(indicator_analysis_button, candle_analysis_button)



