import os
db = {
    'user': 'root',
    'password': 'ansdjdhkd1',
    'host': os.environ.get('DB_HOST'),
    'port': 3306,
    'database': 'miniter'
}
# DB URL
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

# JWT KEY
JWT_SECRET_KEY = "aaaaaaaaaaaaaaaaaaa"

# PROFILE IMAGE PATH
UPLOAD_FOLDER = './profile_images'
