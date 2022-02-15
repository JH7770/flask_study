import os
import sys
import pytest
import bcrypt

from flask import json
from .config import test_config

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from app_init import create_app

# database engine
database = create_engine(test_config['DB_URL'], encoding='utf-8', max_overflow=0)

"""
fixure decorator가 적용된 함수와 같은 이름의 인자(parameter)가 
다른 test 함수에 지정되어 있으면 pytest가 알아서 같은 이름의 함수의 리턴 값을 해당 인자에 넣어줌
"""


@pytest.fixture
def api():  # fixture 함수 이름
    app = create_app(test_config)
    app.config['TEST'] = True  # 불필요한 메시지는 출력되지 않도록함
    api = app.test_client()  # test용 클라이언트 생성

    return api


def setup_function():
    """
    Pytest 실행 시 실행, userid 2개 생성 및 tweet 1개 생ㅅ어
    :return: None
    """
    # 2개 user 생성
    hasshed_password = bcrypt.hashpw(b"test", bcrypt.gensalt())
    new_users = [
        {
            'id': 1,
            'name': "name2",
            'email': 'test@test.test',
            'profile': 'test',
            'hashed_password': hasshed_password
        },
        {
            'id': 2,
            'name': "name1",
            'email': 'test2@test.test',
            'profile': 'test',
            'hashed_password': hasshed_password
        },
    ]

    database.execute(text("""
        INSERT INTO users (
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id, 
            :name, 
            :email, 
            :profile, 
            :hashed_password
        )"""), new_users)
    # user2에 tweet 하나 생성
    database.execute(text("""
        INSERT INTO tweets(
            user_id,
            tweet
        ) VALUES (
            2,
            "Hello World"
        )
        
    """))


def teardown_function():
    """
    pytest 종료 시 실행
    :return: None
    """
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):  # 위에서 설정한 fixure를 여기서 사용(인자 api)
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_login(api):
    """
    Login test (로그인 후 Access Token 확인)
    :param api: testClient
    :return:
    """
    login_user = {
        'email': 'test@test.test',
        'password': 'test'
    }
    resp = api.post(
        '/user/login',
        data=json.dumps(login_user),
        content_type='application/json'
    )
    assert b"access_token" in resp.data


def test_unauthorized(api):
    """
    Endpoint의 자격 증명 절차 확인
    :param api: test client
    :return:
    """

    # url : /tweet/tweet
    tweet_data = {
        'tweet': 'hello'
    }
    resp = api.post(
        '/tweet/tweet',
        data=json.dumps(tweet_data),
        content_type='application/json'
    )
    assert resp.status_code == 401

    # url : /tweet/timeline
    resp = api.get(
        '/tweet/timeline'
    )
    assert resp.status_code == 401

    # url : /tweet/follow
    follow_data = {
        'id': 1,
    }
    resp = api.post(
        '/tweet/follow',
        data=json.dumps(follow_data),
        content_type='application/json'
    )
    assert resp.status_code == 401

    # url : /tweet/unfollow
    unfollow_data = {
        'id': 1,
    }
    resp = api.post(
        '/tweet/unfollow',
        data=json.dumps(unfollow_data),
        content_type='application/json'
    )
    assert resp.status_code == 401

def test_login(api):
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
    assert resp.status_code == 200


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
    print(resp.data)
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


def test_follow_and_unfollow(api):
    """
    follow/unfollow Test
    :param api: test client
    :return:
    """

    # 로그인
    resp = api.post(
        '/user/login',
        data=json.dumps(
            {'email': 'test@test.test', 'password': 'test'}
        ),
        content_type='application/json'
    )

    assert b'access_token' in resp.data
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # 사용자 1의 timeline 확인
    resp = api.get(
        f'/tweet/timeline',
        headers={'Authorization': access_token}
    )
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_name': 'name2',
        'user_id': 1,
        'timeline': []
    }

    # 사용자 2 follow
    resp = api.post(
        '/tweet/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 사용자 1의 타임라인에 사용자 2의 tweet이 있는 것을 확인

    resp = api.get(
        f'/tweet/timeline',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    tweets = json.loads(resp.data.decode('utf-8'))
    assert tweets == {
        'user_name': 'name2',
        'user_id': 1,
        'timeline': [
            {
                'tweet': "Hello World",
                'user_id': 2
            }
        ]
    }

    # 사용자 2를 unfollow
    resp = api.post(
        '/tweet/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200
    # 사용자 1의 timeline 확인
    resp = api.get(
        f'/tweet/timeline',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    tweets = json.loads(resp.data.decode('utf-8'))
    assert tweets == {
        'user_name': 'name2',
        'user_id': 1,
        'timeline': []
    }

