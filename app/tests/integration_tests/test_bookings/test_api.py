import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, bookings_quantity",
    [
        *[(4, "2024-01-01", "2024-01-07", 200, i) for i in range(2, 10)],
        (4, "2024-01-01", "2024-01-07", 409, 9),
        (4, "2024-01-01", "2024-01-07", 409, 9),
    ],
)
async def test_get_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    status_code,
    bookings_quantity,
    authenticated_ac: AsyncClient,
):

    response_new_booking = await authenticated_ac.post(
        "/v1/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response_new_booking.status_code == status_code

    response_user_bookings = await authenticated_ac.get("/v1/bookings")

    assert len(response_user_bookings.json()) == bookings_quantity


# async def test_delete_booking(authenticated_ac: AsyncClient):
#     await authenticated_ac.delete(
#         "/bookings",
#         params={"room_id": 4}
#     )


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Республика Коми", "2023-05-03", "2023-05-05", 200),
        ("Республика Коми", "2023-05-03", "2023-04-05", 400),
        ("Республика Коми", "2023-05-03", "2023-05-02", 400),
        ("Республика Коми", "2023-05-03", "2023-06-02", 200),
        ("Республика Коми", "2023-05-03", "2023-06-03", 400),
    ],
)
async def test_get_hotels_by_location_and_time(
    location,
    date_from,
    date_to,
    status_code,
    authenticated_ac,
):
    response = await authenticated_ac.get(
        f"/v1/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):

    response_get = await authenticated_ac.get("/v1/bookings")
    assert response_get.status_code == 200
    assert len(response_get.json()) > 0

    response_delete = await authenticated_ac.delete(
        "/v1/bookings", params={"bookings_id": 1}
    )
    assert response_delete.status_code == 200

    response_get2 = await authenticated_ac.get("/v1/bookings")
    assert response_get2.status_code == 200
    assert len(response_get2.json()) == len(response_get.json()) - 1

    response_add = await authenticated_ac.post(
        "/v1/bookings",
        params={
            "room_id": response_delete.json()["room_id"],
            "date_from": response_delete.json()["date_from"],
            "date_to": response_delete.json()["date_to"],
        },
    )
    assert response_add.status_code == 200
    assert response_add is not None

    response_get3 = await authenticated_ac.get("/v1/bookings")
    assert response_get3.status_code == 200
    assert len(response_get3.json()) == len(response_get.json())
