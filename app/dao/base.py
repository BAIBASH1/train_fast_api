"""
Base Data Access Object (DAO) class.

This class provides generic methods for performing CRUD operations on the database.
It is designed to be inherited by other DAO classes, which will define the `model` attribute
to specify the model they interact with. The class includes methods for finding records by ID,
finding records by filters, retrieving all records, adding new records, and deleting records.
"""

from sqlalchemy import delete, insert, select

from app.database import async_session_maker


class BaseDAO:
    """
    Base Data Access Object class for interacting with the database.

    This class provides common CRUD operations for interacting with the database. It should be
    inherited by specific DAO classes that define a `model` attribute (representing the table
    to interact with). The methods include:
        - find_by_id: Retrieve a record by its ID.
        - find_one_or_none: Retrieve a record by filtering based on specified criteria.
        - find_all: Retrieve all records that match given filter criteria.
        - add: Add a new record to the database.
        - delete: Delete records based on specified filter criteria.

    Attributes:
        model (Base): The SQLAlchemy model class that this DAO operates on. It should be set by the subclass.
    """

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        """
        Retrieve a record by its ID.

        Args:
            model_id (int): The ID of the record to retrieve.

        Returns:
            dict | None: The record as a dictionary if found, otherwise None.
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Retrieve a single record based on filter criteria.

        Args:
            filter_by: Keyword arguments representing filter criteria (example: `{"id": 1}`).

        Returns:
            dict | None: The record as a dictionary if found, otherwise None.
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Retrieve all records that match the specified filter criteria.

        Args:
            filter_by: Keyword arguments representing filter criteria (example: `{"id": 1}`).

        Returns:
            list[dict]: A list of records as dictionaries.
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """
        Add a new record to the database.

        Args:
            data: The data to insert into the record, provided as keyword arguments.

        Returns:
            int: The ID of the newly inserted record.
        """
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            user_id = result.scalar_one()
            return user_id

    @classmethod
    async def delete(cls, **filter_by):
        """
        Delete records that match the specified filter criteria.

        Args:
            filter_by: Keyword arguments representing filter criteria (example: `{"id": 1}`).

        Returns:
            dict | None: The deleted record as a dictionary, or None if no record was found.
        """
        async with async_session_maker() as session:
            query = (
                delete(cls.model).filter_by(**filter_by).returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            deleted = result.scalars().one_or_none()
            return deleted
