from datetime import datetime, timedelta

import pytest
from hamcrest import assert_that, has_properties, has_length, none, not_, is_

from db.models import User, Message, Topic, Prefix, ModelInput


class TestUser:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        pass

    def test_get_create_create_user(self, session):
        user = User.get_create(
            user_id=123,
            nickname='user1',
            name='handsome user',
            tire=1,
            is_admin=True,
            messages_limit=10,
            model_input='user1 model input'
        )
        assert_that(session.query(User).count(), is_(1))
        assert_that(user, has_properties(
            user_id=123,
            nickname='user1',
            name='handsome user',
            tire=1,
            is_admin=True,
            messages_limit=10,
            enabled=True,
            is_deleted=False,
            created_at=not_(none())
        ))

        assert_that(user.model_inputs, has_length(1))
        assert_that(user.model_inputs[0], has_properties(
            user_id=123,
            model_name='user1 model input',
            is_deleted=False,
        ))

    def test_get_create_get_user(self, session):
        user = User(
            user_id=123,
            nickname='user1',
            name='handsome user',
            tire=1,
            is_admin=True,
            messages_limit=10,
        )
        session.add(user)
        session.commit()
        assert_that(session.query(User).count(), is_(1))

        user = User.get_create(
            user_id=123,
            nickname='another.user',
            name='new handsome user',
            tire=0,
            is_admin=False,
            messages_limit=11,
            model_input='another user model input'
        )
        assert_that(session.query(User).count(), is_(1))
        assert_that(user, has_properties(
            user_id=123,
            nickname='user1',
            name='handsome user',
            tire=1,
            is_admin=True,
            messages_limit=10,
            enabled=True,
            is_deleted=False,
            created_at=not_(none())
        ))

    def test_get_users_created_for_last_days(self, session):
        users = [User.get_create(user_id) for user_id in range(1, 11)]
        for user in users[:4]:
            user.created_at = datetime.now() - timedelta(days=10)
        session.commit()

        assert_that(User.get_users_created_for_last_days(5), is_(6))
        assert_that(User.get_users_created_for_last_days(15), is_(10))

    def test_clear_user_history(self, session):
        user1 = User.get_create(1, model_input='Model input for user1')
        user2 = User.get_create(2, model_input='Model input for user2')

        for user in (user1, user2):
            Message.add_user_message(user.user_id, f'Message from user {user.user_id}')
            Message.add_bot_message(user.user_id, f'Message to user {user.user_id} from bot')
            Topic.add(user.user_id, f'Topic for user {user.user_id}')
            Prefix.add(user.user_id, f'Prefix for user {user.user_id}')

        User.clear_user_history(user1.user_id)
        for user, is_deleted_user in ((user1, True),
                                      (user2, False)):
            assert_that(session.query(User).filter(User.user_id == user.user_id, User.is_deleted == False).count(), is_(1))
            assert_that(session.query(User).filter(User.user_id == user.user_id, User.is_deleted == True).count(), is_(0))

            for model, expected_count in ((ModelInput, 1),
                                          (Message, 2),
                                          (Topic, 1),
                                          (Prefix, 1)):
                assert_that(session.query(model).filter(model.user_id == user.user_id, model.is_deleted == is_deleted_user).count(), is_(expected_count))
                assert_that(session.query(model).filter(model.user_id == user.user_id, model.is_deleted == (not is_deleted_user)).count(), is_(0))
