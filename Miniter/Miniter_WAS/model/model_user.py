from common import db
from sqlalchemy import text


class UserModel:
    def __init__(self):
        self.db = db.get_db()

    def insert_user(self, new_user_info):
        if 'name' not in new_user_info:
            raise Exception("insert_user() : 'name' is Missing...")
        if 'email' not in new_user_info:
            raise Exception("insert_user() : 'email' is Missing...")
        if 'profile' not in new_user_info:
            raise Exception("insert_user() : 'profile' is Missing...")
        if 'password' not in new_user_info:
            raise Exception("insert_user() : 'password' is Missing...")

        return self.db.execute(text("""
            INSERT INTO users(
            name,
            email,
            profile,
            hashed_password) VALUES (
            :name,
            :email,
            :profile,
            :password
            )
        """), new_user_info).lastrowid

    def get_user_from_id(self, user_id):
        row = self.db.execute(text("""
                SELECT
                    id,
                    name,
                    email,
                    profile
                FROM users
                WHERE id = :user_id
            """), {
            'user_id': user_id
        }).fetchone()

        return {
            'id': row['id'],
            'name': row['name'],
            'email': row['email'],
            'profile': row['profile']
        } if row else None

    def get_user_from_email(self, email):
        return self.db.execute(text("""
            SELECT 
                id,
                hashed_password
            FROM users
            WHERE email =:email
        """), {'email': email}).fetchone()

    def insert_profile_picture(self, profile_picture_path, user_id):
        return self.db.execute(text("""
            UPDATE users
            SET profile_picture =:profile_picture_path,
            WHERE id =:user_id
        """), {
            'user_id': user_id,
            'profile_picture_path': profile_picture_path
        }).rowcount

    def get_profile_picture_path(self, user_id):
        return self.db.execute(text("""
            SELECT profile_picture
            FROM users
            WHERE id =:user_id
        """),{
            'user_id':user_id
        }).fetchone()