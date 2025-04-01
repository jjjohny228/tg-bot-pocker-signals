from aiogram import Dispatcher
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
import asyncio


def rate_limit(limit: float, key=None):
    """
    Декоратор для конфигурации лимита и ключей для своих функций.
    :param limit: секунды
    :param key: ключ
    :return: Callable
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=0.8, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        # Получаем текущий хэндлер
        handler = current_handler.get()
        # Получаем диспетчер из контекста
        dispatcher = Dispatcher.get_current()

        # Если хэндлер был настроен, получаем частотный лимит и ключ хэндлера
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            # Отменяем выполнение хэндлера
            raise CancelHandler()

    async def message_throttled(self, message: Message, throttled: Throttled):
        """
        Уведомлять пользователя только при первом превышении и уведомлять о разблокировке только при последнем превышении

        :param message:
        :param throttled:
        """
        # Вычисляем, сколько нужно подождать перед концом блокировки
        delta = throttled.rate - throttled.delta

        # Предотвращаем флуд
        if throttled.exceeded_count <= 2:
            await message.reply('Please, not so often 🙏')

        # Ждём
        await asyncio.sleep(delta)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        # Если хэндлер был настроен, получаем частотный лимит и ключ
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.callback_query_throttled(query, t)
            # Отменяем выполнение хэндлера
            raise CancelHandler()

    async def callback_query_throttled(self, query: CallbackQuery, throttled: Throttled):
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await query.answer('Please, not so often 🙏', show_alert=True)

        await asyncio.sleep(delta)


def setup_middleware(dp):
    dp.middleware.setup(ThrottlingMiddleware())
