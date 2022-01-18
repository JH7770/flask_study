db = {
    'user': 'root',
    'password': 'ansdjdhkd1',
    'host': 'localhost',
    'port': 3306,
    'database': 'miniter'
}

JWT_SECRET_KEY = "aaaaaaaaaaaaaaaaaaa"
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
