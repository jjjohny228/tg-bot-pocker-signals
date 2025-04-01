from typing import Generator
from datetime import datetime, timedelta

from .models import User, PocketId
from .reflink import increase_users_count


# region SQL Create

def create_user_if_not_exist(telegram_id: int, name: str, reflink: str = None) -> User:
    user = get_user_by_telegram_id_or_none(telegram_id)
    if not user:
        user = User.create(name=name, telegram_id=telegram_id, referral_link=reflink)
        increase_users_count(reflink=reflink)
    return user


# endregion


# region SQL Select


def get_users_total_count() -> int:
    return User.select().count()


def get_users_by_hours(hours: int):
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_ids() -> Generator:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> tuple:
    yield from ((user.telegram_id, user.name, user.referral_link, user.registration_timestamp, user.pocket_id) for
                user in User.select())


def get_user_by_telegram_id_or_none(telegram_id: int) -> None | User:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_user_pocket_id(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).pocket_id


# endregion


# region Update


def set_pocket_id(pocket_id: int):
    PocketId.create(pocket_id=pocket_id)


def check_pocket_id(pocket_id: int):
    pocket_object = PocketId.get_or_none(pocket_id=pocket_id)
    return pocket_object is not None


def set_user_pocket_id(telegram_id: int, pocket_id: int):
    User.update(pocket_id=pocket_id).where(User.telegram_id == telegram_id).execute()


def set_pocket_deposit(pocket_id: int):
    user, created = User.get_or_create(pocket_id=pocket_id, defaults={'deposit': True})
    if not created:
        user.deposit = True
        user.save()


def check_user_deposit(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).deposit


def check_has_user_pocket_id_and_deposit(user: User) -> bool:
    return user.pocket_id is not None and user.deposit is True

# endregion
