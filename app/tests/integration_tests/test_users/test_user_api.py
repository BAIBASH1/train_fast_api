import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("new_user@mail.ru", "seconduser", 200),
        ("new_user@mail.ru", "paaaaass2", 409),
        ("new_user@mail.ru", "paaaaass2", 409),
        ("new_usermail.ru", "paaaaass2", 422),
    ],
)
async def test_register_user(
    ac: AsyncClient,
    db_transaction: AsyncSession,
    email: str,
    password: str,
    status_code: int,
):
    response = await ac.post(
        "/v1/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("firstuser@user.ru", "firstuser", 200),
        ("firstuser@user.ru", "firstuser2", 401),
        ("firstuser2@user.ru", "firstuser", 401),
        ("seconduser@user.ru", "seconduser", 200),
        ("seconduser2@user.ru", "seconduser", 401),
        ("seconduser@user.ru", "seconduser2", 401),
    ],
)
async def test_login_user(
    ac: AsyncClient, email: str, password: str, status_code: int
):
    response = await ac.post(
        "/v1/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == status_code
