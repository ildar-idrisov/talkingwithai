import pytest
from hamcrest import assert_that, contains_inanyorder, has_properties, is_

from db.models import Prefix, User


class TestPrefix:

    @pytest.fixture(autouse=True)
    def environment(self, session):
        pass

    def test_add_prefix(self, session):
        user = User(user_id=123)
        session.add(user)
        session.commit()

        Prefix.add(user_id=user.user_id, prefix='User prefix #1')
        Prefix.add(user_id=user.user_id, prefix='User prefix #2')
        topics = session.query(Prefix).all()
        assert_that(topics, contains_inanyorder(
            has_properties(user_id=user.user_id, prefix='User prefix #1', is_deleted=False),
            has_properties(user_id=user.user_id, prefix='User prefix #2', is_deleted=False),
        ))

    def test_get_for_user(self, session):
        user = User(user_id=123)
        user2 = User(user_id=124)
        prefix1 = Prefix(user_id=user.user_id, prefix='User1 prefix #1')
        prefix2 = Prefix(user_id=user.user_id, prefix='User1 prefix #2')
        deleted_prefix2 = Prefix(user_id=user.user_id, prefix='User1 deleted prefix', is_deleted=True)
        prefix1_user2 = Prefix(user_id=user2.user_id, prefix='User2 prefix #1')
        session.add_all([user, user2, prefix1, prefix2, deleted_prefix2, prefix1_user2])
        session.commit()

        assert_that(Prefix.get_for_user(user.user_id), contains_inanyorder(prefix1.prefix, prefix2.prefix))
        assert_that(Prefix.get_for_user(user2.user_id), contains_inanyorder(prefix1_user2.prefix))

    def test_delete_persona(self, session):
        user = User(user_id=123)
        prefix1 = Prefix(user_id=user.user_id, prefix='User1 prefix #1')
        prefix2 = Prefix(user_id=user.user_id, prefix='your persona: User1 prefix #2')
        prefix3 = Prefix(user_id=user.user_id, prefix='User1 YoUr pERSOna: prefix #2')
        deleted_prefix = Prefix(user_id=user.user_id, prefix='your persona: User1 deleted prefix', is_deleted=True)
        session.add_all([user, prefix1, prefix2, prefix3, deleted_prefix])
        session.commit()

        Prefix.delete_persona(user.user_id)
        assert_that(prefix1.is_deleted, is_(False))
        assert_that(prefix2.is_deleted, is_(True))
        assert_that(prefix3.is_deleted, is_(True))
        assert_that(deleted_prefix.is_deleted, is_(True))
