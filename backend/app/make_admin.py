"""Promote an existing user to admin.

Usage (from the backend folder):  python -m app.make_admin someone@example.com
"""
import sys

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import User


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m app.make_admin <email>")

    Base.metadata.create_all(bind=engine)
    email = sys.argv[1].strip().lower()
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            sys.exit(f"No user with email {email}. Register first.")
        user.is_admin = True
        db.commit()
    print(f"{email} is now an admin.")


if __name__ == "__main__":
    main()