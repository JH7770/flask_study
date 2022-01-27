from flask import current_app, jsonify
from sqlalchemy import text


def insert_user(new_user):
    return current_app.database.execute(text("""
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
    """), new_user).lastrowid


def get_user_from_id(user_id):
    row = current_app.database.execute(text("""
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


def get_user_from_email(email):
    return current_app.database.execute(text("""
        SELECT 
            id,
            hashed_password
        FROM users
        WHERE email =:email
    """), {'email': email}).fetchone()
