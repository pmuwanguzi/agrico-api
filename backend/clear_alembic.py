#!/usr/bin/env python
"""Clear stale Alembic version entries from the database."""
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("DELETE FROM alembic_version"))
        db.session.commit()
        print("✓ Cleared alembic_version table successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Table may not exist yet, which is fine.")
