# test_db = {
#     'user': 'test',
#     'password': 'password',
#     'host': 'localhost',
#     'port': 3306,
#     'database': 'tset_db'
# }
test_db = {
    'user': 'root',
    'password': 'ansdjdhkd1',
    'host': 'localhost',
    'port': 3306,
    'database': 'test'
}

test_config = {
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@"
              f"{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8"
}
