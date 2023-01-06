import pytest
from hamcrest import assert_that, contains_inanyorder, has_properties

from db.models import Topic, User


class TestTopic:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        pass

    def test_add_topic(self, session):
        user = User(user_id=123)
        session.add(user)
        session.commit()

        Topic.add(user_id=user.user_id, topic='User topic #1')
        Topic.add(user_id=user.user_id, topic='User topic #2')
        topics = session.query(Topic).all()
        assert_that(topics, contains_inanyorder(
            has_properties(user_id=user.user_id, topic='User topic #1', is_deleted=False),
            has_properties(user_id=user.user_id, topic='User topic #2', is_deleted=False),
        ))
