from src.database.models import User, register_models
from src.database.user import check_has_user_pocket_id_and_deposit

register_models()
User.update(deposit=True, pocket_id=None).where(User.telegram_id == 1234).execute()
user = User.get(User.telegram_id == 1234)
print(check_has_user_pocket_id_and_deposit(user))