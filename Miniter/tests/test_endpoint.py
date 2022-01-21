`import os
import sys
import pytest
import bcrypt

from flask import json
from config import test_config

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app import app
from sqlalchemy import create_engine, text

database = create_engine(test_config['DB_URL'], encoding='utf-8', max_overflow=0)

"""
fixure decorator가 적용된 함수와 같은 이름의 인자(parameter)가 
다른 test 함수에 지정되어 있으면 pytest가 알아서 같은 이름의 함수의 리턴 값을 해당 인자에 넣어줌
"""


@pytest.fixture
def api():  # fixture 함수 이름
    app.config['TEST'] = True  # 불필요한 메시지는 출력되지 않도록함
    api = app.test_client()  # test용 클라이언트 생성

    return api


def setup_function():
    # sign up
    new_user = {
        'id': 1,
        'name': "test",
        'email': 'test@test.test',
        'profile': 'test'
    }
    new_user['hashed_password'] = bcrypt.hashpw(b"test", bcrypt.gensalt())
    database.execute(text("""
        INSERT INTO users (
            id, name, email, profile, hashed_password
        ) VALUES (
            :id, :name, :email, :profile, :hashed_password
        )
    """), new_user)


def testdown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):  # 위에서 설정한 fixure를 여기서 사용(인자 api)
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_tweet(api):
    # test user 생성
    new_user = {
        'email': 'test@test.test',
        'password': 'test',
        'name': "test",
        'profile': 'test'
    }

    # login
    resp = api.post(
        '/user/login',
        data=json.dumps({
            'email': new_user['email'],
            'password': new_user['password'],
        }),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # tweet
    resp = api.post(
        '/tweet/tweet',
        data=json.dumps({'tweet': 'Hello'}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # tweet 확인
    resp = api.get(
        f'/tweet/timeline',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200
    tweets = json.loads(resp.data.decode('utf-8'))
    assert tweets['timeline'][0]['tweet'] == 'Hello'
`