from datetime import datetime, timedelta

import pytest
from hamcrest import assert_that, has_properties, has_length, none, not_, is_, contains_inanyorder

from db.models import User, Message, Topic, Prefix, ModelInput


class TestAddMessage:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        self.user = User.get_create(123)

    def test_add_bot_message(self, session):
        message = Message.add_bot_message(
            user_id=self.user.user_id,
            content='A message from the bot'
        )
        assert_that(session.query(Message).count(), is_(1))
        assert_that(message, has_properties(
            user_id=self.user.user_id,
            content='A message from the bot',
            is_from_user=False,
            timestamp=not_(none()),
            is_deleted=False
        ))

    def test_add_user_message(self, session):
        message = Message.add_user_message(
            user_id=self.user.user_id,
            content='A message from the user'
        )
        assert_that(session.query(Message).count(), is_(1))
        assert_that(message, has_properties(
            user_id=self.user.user_id,
            content='A message from the user',
            is_from_user=True,
            timestamp=not_(none()),
            is_deleted=False
        ))


class TestMessage:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        self.non_existing_user_id = 124
        self.user = User(user_id=123)
        self.bot_message1 = Message(
            user_id=self.user.user_id,
            content='The first message from the bot',
            is_from_user=False,
        )
        self.bot_message2 = Message(
            user_id=self.user.user_id,
            content='The second message from the bot',
            is_from_user=False,
        )
        self.bot_message3 = Message(
            user_id=self.user.user_id,
            content='The third message from the bot',
            is_from_user=False,
        )
        self.deleted_bot_message = Message(
            user_id=self.user.user_id,
            content='The deleted message from the bot',
            is_from_user=False,
            is_deleted=True,
        )
        self.user_message1 = Message(
            user_id=self.user.user_id,
            content='The first message from the user',
            is_from_user=True,
        )
        self.user_message2 = Message(
            user_id=self.user.user_id,
            content='The second message from the user',
            is_from_user=True,
        )
        self.deleted_user_message = Message(
            user_id=self.user.user_id,
            content='The deleted message from the user',
            is_from_user=True,
            is_deleted=True,
        )
        session.add_all([self.user, self.bot_message1, self.bot_message2, self.user_message1, self.user_message2,
                         self.bot_message3, self.deleted_bot_message, self.deleted_user_message])
        session.commit()

    def test_get_bot_messages_for_user(self, session):
        messages = Message.get_bot_messages_for_user(self.user.user_id)
        assert_that(messages, has_length(3))
        assert_that(messages, contains_inanyorder(self.bot_message1.content, self.bot_message2.content, self.bot_message3.content))
        assert_that(Message.get_bot_messages_for_user(self.non_existing_user_id), has_length(0))

    def test_get_user_messages_for_user(self, session):
        messages = Message.get_user_messages_for_user(self.user.user_id)
        assert_that(messages, has_length(2))
        assert_that(messages, contains_inanyorder(self.user_message1.content, self.user_message2.content))
        assert_that(Message.get_user_messages_for_user(self.non_existing_user_id), has_length(0))


class TestMessageHelpers:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        self.user1 = User(user_id=123)
        self.user2 = User(user_id=124)
        self.user3 = User(user_id=125)
        self.bot_message_user1_10_minutes = Message(
            user_id=self.user1.user_id,
            content='The first message from the bot',
            is_from_user=False,
            timestamp=datetime.now() - timedelta(minutes=10),
        )
        self.bot_message_user1_2_days = Message(
            user_id=self.user1.user_id,
            content='The second message from the bot',
            is_from_user=False,
            timestamp=datetime.now() - timedelta(minutes=20),
        )
        self.bot_message_user2_2_days = Message(
            user_id=self.user2.user_id,
            content='The third message from the bot',
            is_from_user=False,
            timestamp=datetime.now() - timedelta(minutes=30),
        )
        self.deleted_bot_message = Message(
            user_id=self.user3.user_id,
            content='The deleted message from the bot',
            is_from_user=False,
            is_deleted=True,
            timestamp=datetime.now() - timedelta(minutes=5),
        )
        self.user_message_user1_10_minutes = Message(
            user_id=self.user1.user_id,
            content='The first message from the user',
            is_from_user=True,
            timestamp=datetime.now() - timedelta(days=2),
        )
        self.user_message_user1_2_days = Message(
            user_id=self.user1.user_id,
            content='The second message from the user',
            is_from_user=True,
            timestamp=datetime.now() - timedelta(days=2),
        )
        self.user_message_user2_2_days = Message(
            user_id=self.user2.user_id,
            content='The third message from the user',
            is_from_user=True,
            timestamp=datetime.now() - timedelta(days=5),
        )
        self.deleted_user_message = Message(
            user_id=self.user3.user_id,
            content='The deleted message from the user',
            is_from_user=True,
            is_deleted=True,
            timestamp=datetime.now() - timedelta(minutes=5),
        )
        session.add_all([self.user1, self.user2, self.user3, self.bot_message_user1_10_minutes,
                         self.bot_message_user1_2_days, self.bot_message_user2_2_days, self.deleted_bot_message,
                         self.user_message_user1_10_minutes, self.user_message_user1_2_days,
                         self.user_message_user2_2_days, self.deleted_user_message])
        session.commit()

    def test_get_active_users_for_last_days(self, session):
        # considered self.deleted_user_message only
        assert_that(Message.get_active_users_for_last_days(1), is_(1))

        # considered self.deleted_user_message and messages from the user1
        assert_that(Message.get_active_users_for_last_days(3), is_(2))

        # considered self.deleted_user_message and messages from the user1 and user2
        assert_that(Message.get_active_users_for_last_days(6), is_(3))

    def test_messages_count_for_last_x_minutes(self, session):
        # considered self.deleted_user_message only
        assert_that(Message.messages_count_for_last_x_minutes(60), is_(1))

        # considered self.deleted_user_message and messages from the user1
        assert_that(Message.messages_count_for_last_x_minutes(60 * 24 * 3), is_(3))  # 3 days

        # considered self.deleted_user_message and messages from the user1 and user2
        assert_that(Message.messages_count_for_last_x_minutes(60 * 24 * 6), is_(4))  # 6 days
