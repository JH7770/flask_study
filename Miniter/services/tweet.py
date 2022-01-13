from flask import current_app, request
from sqlalchemy import text


def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
        INSERT INTO tweets(
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount


def insert_follow(user_follow):
    return current_app.database.execute(text("""
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow
        )
    """), user_follow).rowcount


def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
                DELETE FROM users_follow_list 
                WHERE user_id = :id
                AND follow_user_id = :unfollow
            """), user_unfollow).rowcount
    return '', 200

def get_timeline(user_id):
    rows = current_app.database.execute(text("""
        SELECT
            t.user_id,
            t.tweet
        FROM tweets t 
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id 
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """), {
    'user_id': user_id
    }).fetchall()

    return [{
        'user_id': row['user_id'],
        'tweet': row['tweet']
    } for row in rows]

