"""
Data Access Object for Users.

This module defines the `UsersDAO` class, which provides asynchronous methods for interacting
with the `Users` model, including checking user existence and performing database operations.
"""

from app.dao.base import BaseDAO
from app.users.user_models import Users


class UsersDAO(BaseDAO):
    model = Users
