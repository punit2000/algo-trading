"""
app.database — Database session and engine management.

Implemented in M1+.

Uses SQLAlchemy 2.x async engine with asyncpg driver.
Alembic manages schema migrations (see migrations/).

Connection string format:
    postgresql+asyncpg://user:password@host:port/dbname

Loaded from settings.db_url (never hard-coded).
"""
