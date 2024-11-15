from __future__ import with_statement
import sys
import os
from logging.config import fileConfig

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from alembic import context
from models import db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Import the models for Alembic to detect
from models import User, Property

# Set the metadata for Alembic to use
target_metadata = db.metadata

def run_migrations_online():
    # connects to the database, then runs migrations
    connectable = db.engine
    context.configure(
        connection=connectable,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

# Call the function to run migrations
run_migrations_online()

