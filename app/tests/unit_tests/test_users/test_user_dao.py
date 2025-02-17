import pytest

from app.users.user_dao import UsersDAO


@pytest.mark.parametrize(
    "user_id, is_present, email",
    [
        (1, True, "firstuser@user.ru"),
        (2, True, "seconduser@user.ru"),
        (3, False, "fisdfsf@user.ru"),
    ],
)
async def test_find_by_id(user_id, is_present, email):
    user = await UsersDAO.find_by_id(user_id)
    if is_present:
        assert user.email == email
        assert user.id == user_id
    else:
        assert user is None
