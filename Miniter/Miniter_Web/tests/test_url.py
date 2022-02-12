import pytest
from app_init import create_app

@pytest.fixture
def api():  # fixture 함수 이름
    app = create_app()
    app.config['TEST'] = True  # 불필요한 메시지는 출력되지 않도록함
    api = app.test_client()  # test용 클라이언트 생성

    return api

def test_url_endpoint(api):
    resp = api.get('/')
    assert resp.status_code == 200

    resp = api.get('/login')
    assert resp.status_code == 200

    resp = api.get('/sign-up')
    assert resp.status_code == 200

    resp = api.get('/tweets')
    assert resp.status_code == 200

