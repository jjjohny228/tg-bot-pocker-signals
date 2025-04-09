import os

from aiogram.types import Message
from typing import Literal
from dotenv import load_dotenv
from aiogram.utils.markdown import link, bold, underline

load_dotenv()

class Messages:
    bot_name = os.getenv("BOT_NAME")
    @staticmethod
    def get_welcome_message(message: Message) -> str:
        text = f"""
        👋Hi, {message.from_user.username}!💲

🚀Welcome to the best trading robot {os.getenv('BOT_NAME')} on binary options with the highest passability of signals on the market >97,89%.

💰 The bot has a unique algorithm based on AI GPT 4.0 which will analyze the market and give a signal.

🏆{os.getenv('BOT_NAME')} is the industry leader in binary options trading robots🏆

🔑 Activate the bot absolutely free and change your trading to a new high level with go plus➕
        """
        return text

    @staticmethod
    def get_welcome_photo() -> str:
        return 'https://habrastorage.org/webt/7a/rf/ef/7arfefinfjvghftktj3cif-qpig.jpeg'

    @staticmethod
    def get_benefit_message() -> str:
        text = """
        ❔What I get by activating the bot❔

🚀Workspace with more than 100 assets of Pocket Option broker and signal passability >97,89%.

🔐Access to a closed community of successful traders, where I give out my personal signals every day at 20:30 New York time.

🔎 Advanced Algorithm 2.0, which will analyze all indicators and give a signal with detailed analytics.

🏆Exclusive training material on trading for successful trading on Pocket Option.
"""
        return text

    @staticmethod
    def get_benefit_photo() -> str: # нет этой фотки
        return 'https://habrastorage.org/webt/ma/dr/d8/madrd8yj4ums41si4cjabr2ybcg.jpeg'

    @staticmethod
    def get_registration_message() -> str:
        text = f"""
        🔑To get full access to Go Plus robot with more than 100 assets, you need to create a new account on Pocket Option broker strictly by following the <a href='{os.getenv('REF_URL')}'>link</a> 🔗

❗️Attention! Register your account strictly by following the <a href='{os.getenv('REF_URL')}'>link</a> below. Otherwise the bot will not be able to verify the account and you will not get access to the bot go plus❗️.

⚠️Important: do not give your ID to anyone, as the bot is issued only for 1 account❕
"""
        return text

    @staticmethod
    def get_ask_for_pocket_id_message() -> str:
        text = """
        🚀Send your Pocket Option account ID in the message below👇

⚠️Important: ID should be sent in numbers only - no letters❕️
"""
        return text

    @staticmethod
    def get_bullshit_registration_message() -> str:
        text = "❕ You sent something you don't understand! The pocket option account ID consists of 8 digits."
        return text

    @staticmethod
    def get_registration_photo() -> str:
        return 'https://habrastorage.org/webt/qt/y2/42/qty242l5suevnlczk-p9plfzxq4.jpeg'

    @staticmethod
    def get_invalid_registration_photo() -> str:
        return 'https://habrastorage.org/webt/e1/h9/ua/e1h9uaxldpwvseesnibkfiqj5km.png'

    @staticmethod
    def get_registration_fail_message() -> str:
        text = """
        ❌Account not registered by link🔗

❗️Delete old account using the instructions below. After deletion you need to register a new account strictly by following the link - https://bit.ly/pocket-option-rus.

🚀After registration send your new Pocket Option account ID by the message below👇
        """
        return text

    @staticmethod
    def get_deposit_photo() -> str:
        return 'https://habrastorage.org/webt/xd/le/z5/xdlez5lyrfoyyveh7kfvndswdjm.png'

    @staticmethod
    def get_deposit_message() -> str:
        text = """✅Account registered🔗

🔥The last step is left. To activate the best binary options trading robot. Fund your new Pocket Option account with $50💸 or more.

🚀After depositing click the “I funded” button below👇
        """
        return text

    @staticmethod
    def get_invalid_deposit_message() -> str:
        text = """
        ❌Oops! Your Pocket Option account is not funded from 50$❗️

💰Fill up your new account with $50 or more. To activate the best binary options trading robot📈

🚀After depositing click the “I funded” button below👇"""
        return text

    @staticmethod
    def get_successful_deposit_text() -> str:
        text = f"""
        ✅Bot has been successfully activated. Now you have full access to Go Plus robot with more than 100 assets📈

🚀Also don't forget to join the best trading team where I give out my personal signals - {os.getenv('CHANNEL_URL')}

❔If there is any question, feel free to contact me with any questions. I will be glad to communicate - {os.getenv('SUPPORT_USERNAME')}"""
        return text

    @staticmethod
    def get_signals_menu_photo() -> str:
        return 'https://habrastorage.org/webt/xk/2r/kn/xk2rknpivwhyltk8mcgnuidi1rm.jpeg'

    @staticmethod
    def get_signals_menu_message() -> str:
        text = """
        ↓Select trade asset ↓

- Recommended asset: Commodities
- Recommended mode: FIN

⚠️Important: trade with 1-5% of your deposit."""

        return text

    @staticmethod
    def get_currency_pairs_photo(signal_type: str) -> str:
        if signal_type == 'currency':
            return 'https://habrastorage.org/webt/u5/xh/sw/u5xhswau3m0jqqzcos9itgbsqqi.jpeg'
        elif signal_type == 'cryptocurrency':
            return 'https://habrastorage.org/webt/j-/pz/yj/j-pzyjsyr46iwqhxdefqtwoixja.jpeg'
        elif signal_type == 'commodities':
            return 'https://habrastorage.org/webt/sy/b-/n1/syb-n1s8nmvntwvn7zppndv5b3s.jpeg'
        elif signal_type == 'shares':
            return 'https://habrastorage.org/webt/xf/cr/xh/xfcrxh94cccmbwhziy8ae-cber0.jpeg'
        elif signal_type == 'indices':
            return 'https://habrastorage.org/webt/fe/wm/xl/fewmxlsk6ny147utwf84jk-evl0.jpeg'

    @staticmethod
    def get_currency_pairs_message(signal_type: str) -> str:
        text = ''
        if signal_type == 'currency':
            text = """↓Select currency pair ↓

- Recommended pair: USD/BDT OTC
- Profitability: 98%
- Volatility: low

⚠️Important: choose assets with high payout percentage.
"""
        elif signal_type == 'cryptocurrency':
            text = """
            ↓ Choose a cryptocurrency ↓

• Recommended pair: Bitcoin OTC
• Liquidity: 94%
• Volatility: High

⚠️ Important: Select assets with a high payout percentage.
"""
        elif signal_type == 'commodities':
            text = """
            ↓ Choose a commodity ↓

• Recommended pair: Natural Gas OTC
• Liquidity: 95%
• Volatility: Low

⚠️ Important: Select assets with a high payout percentage.
"""
        elif signal_type == 'shares':
            text = """
            ↓ Choose a stock ↓

• Recommended pair: Apple OTC
• Liquidity: 94%
• Volatility: Medium

⚠️ Important: Select assets with a high payout percentage.
"""
        elif signal_type == 'indices':
            text = """
            ↓ Choose an index ↓

• Recommended pair: E50EUR OTC
• Liquidity: 96%
• Volatility: Low

⚠️ Important: Select assets with a high payout percentage.
"""
        return text

    @staticmethod
    def get_analysis_type_message() -> str:
        text = """
        ↓Select type of analysis ↓

- Recommended: indicator

⚠️Important: analyze the chart yourself before getting a signal.
"""
        return text

    @staticmethod
    def get_candle_analysis_message() -> str:
        text = """
        ↓ Select the type of analysis ↓

- **Recommended:** line

⚠️ **Important:** Analyze the chart yourself before receiving a signal.
"""
        return text

    @staticmethod
    def get_indicator_analysis_message() -> str:
        text = """
        ↓Select indicator ↓

- Recommended: MACD

⚠️Important: analyze the chart yourself before getting a signal.
"""
        return text

    @staticmethod
    def get_trade_time_photo() -> str: # нет этого фото
        return 'https://habrastorage.org/webt/wt/ia/4a/wtia4aacdnaf8g-q6sgzrpq4f58.jpeg'

    @staticmethod
    def get_trade_time_message() -> str:
        text = """
        ↓Select trade time ↓

- Recommended time: 2M
- Optimal time: 4M

⚠️Important: the higher the trade time, the higher the signal passibility.
"""
        return text

    @staticmethod
    def get_signal_message(pair_text: str, trade_time: str, open_time: str,
                           global_analysis_type: Literal['candle', 'indicator'], analysis_type: str,
                           trade_move: Literal['Buy', 'Sell']) -> str:
        indicator_text_part = f'📈 Indicator - {analysis_type}' if global_analysis_type == 'indicator' else f'🧨 Candle type - {analysis_type}'
        bot_signal = 'UP ⬆️' if trade_move == 'Buy' else 'DOWN ⬇️'
        text = f"""
        Analysis passed successfully ✅️

💹 OTC Asset: {pair_text}
⌛ Trade Time: {trade_time}
⏱️ Open Time: <b><u>{open_time}</u></b>

📊 Technical Analysis: {trade_move}
🔎 GPT-4.0 Analysis: {trade_move}
{indicator_text_part} : {trade_move}

🚀 Signal from {os.getenv('BOT_NAME')} Bot: {bot_signal}
        """
        return text

    @staticmethod
    def get_signal_photo(trade_move: Literal['Buy', 'Sell']) -> str:
        if trade_move == 'Buy':
            return 'https://habrastorage.org/webt/ou/9v/wm/ou9vwmwzdtyoio5ujdn1vzyk6c4.jpeg'
        elif trade_move == 'Sell':
            return 'https://habrastorage.org/webt/ny/hq/s2/nyhqs2rrwhd4cnsf_plhlhcxvtw.jpeg'

