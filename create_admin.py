"""
One-off CLI script to create the first admin user.

Usage:
    python create_admin.py

You will be prompted for a username and password. Run this locally
pointed at your production DATABASE_URL (via .env) to create the
account that will log into /admin/login on the live site.
"""
import getpass

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.models import AdminUser


def main():
    db = SessionLocal()
    try:
        username = input("Admin username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return

        existing = db.query(AdminUser).filter(AdminUser.username == username).first()
        if existing:
            print(f"A user with username '{username}' already exists.")
            return

        password = getpass.getpass("Admin password: ")
        confirm  = getpass.getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match.")
            return

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return

        admin = AdminUser(
            username=username,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin user '{username}' created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()

# """
# One-off CLI script to create the first admin user.

# Usage:
#     python create_admin.py

# You will be prompted for a username and password. Run this locally
# pointed at your production DATABASE_URL (via .env) to create the
# account that will log into /admin/login on the live site.
# """
# import getpass

# from app.core.database import SessionLocal
# from app.core.security import hash_password
# from app.models.models import AdminUser


# def main():
#     db = SessionLocal()
#     try:
#         username = input("Admin username: ").strip()
#         if not username:
#             print("Username cannot be empty.")
#             return

#         existing = db.query(AdminUser).filter(AdminUser.username == username).first()
#         if existing:
#             print(f"A user with username '{username}' already exists.")
#             return

#         password = getpass.getpass("Admin password: ")
#         confirm  = getpass.getpass("Confirm password: ")

#         if password != confirm:
#             print("Passwords do not match.")
#             return

#         if len(password) < 8:
#             print("Password must be at least 8 characters.")
#             return

#         admin = AdminUser(
#             username=username,
#             hashed_password=hash_password(password),
#             role="admin",
#             is_active=True,
#         )
#         db.add(admin)
#         db.commit()
#         print(f"✓ Admin user '{username}' created successfully.")

#     finally:
#         db.close()


# if __name__ == "__main__":
#     main()
