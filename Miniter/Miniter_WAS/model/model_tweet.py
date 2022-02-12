from common import db
from sqlalchemy import text


class TweetModel:
    def __init__(self):
        self.db = db.get_db()

    def insert_tweet(self, user_tweet):
        if 'id' not in user_tweet:
            raise Exception("Insert_tweet() : id is Missing..")
        if 'tweet' not in user_tweet:
            raise Exception("Insert_tweet() : tweet is Missing")


        return self.db.execute(text("""
            INSERT INTO tweets(
                user_id,
                tweet
            ) VALUES (
                :id,
                :tweet
        )"""), user_tweet).rowcount

    def insert_follow(self, user_follow):
        if 'id' not in user_follow:
            raise Exception("insert_follow() : 'id' is Missing...")

        if 'follow' not in user_follow:
            raise Exception("insert_follow() : 'follow is Missing...")

        return self.db.execute(text("""
               INSERT INTO users_follow_list (
                   user_id,
                   follow_user_id
               ) VALUES (
                   :id,
                   :follow
               )
           """), user_follow).rowcount

    def insert_unfollow(self, user_unfollow):
        if 'id' not in user_unfollow:
            raise Exception("insert_unfollow() : 'id' is Missing..")

        if 'unfollow' not in user_unfollow:
            raise Exception("insert_unfollow() : 'unfollow' is Missing..")


        return self.db.execute(text("""
                    DELETE FROM users_follow_list 
                    WHERE user_id = :id
                    AND follow_user_id = :unfollow
                """), user_unfollow).rowcount

    def get_timeline(self, user_id):
        return self.db.execute(text("""
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