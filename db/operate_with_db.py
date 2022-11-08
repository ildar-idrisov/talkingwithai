from db.models import User
from db_connect import session

users = session.query(User).filter(User.user_id == 1)
if not users.count():
    user1 = User(user_id=1, nickname="User 1")
    user2 = User(user_id=2, nickname="User 2")
    session.add_all([user1, user2])
    session.commit()

users = session.query(User).filter(User.user_id == 1)
for user in users:
    print(f"{user.user_id} => {user.nickname}")