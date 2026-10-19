"""Verify real HTTP responses. Used inside a running Docker container."""
import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, build_opener


def check(base='http://127.0.0.1:8000'):
    client = build_opener(ProxyHandler({}))
    for attempt in range(30):
        try:
            with client.open(base + '/health', timeout=2) as response:
                data = json.load(response)
                assert response.status == 200
                assert response.headers.get_content_type() == 'application/json'
                assert data['status'] == 'ok'
                assert data['environment'] == os.environ.get('APP_ENV', 'development')
            break
        except (OSError, URLError):
            if attempt == 29:
                raise
            time.sleep(1)
    with client.open(base + '/', timeout=3) as response:
        assert response.status == 200
        assert response.headers.get_content_type() == 'text/html'
        body = response.read().decode('utf-8')
        assert 'DevOps Laboratory Work 1' in body
        assert os.environ.get('STUDENT_ID', '38419') in body
    try:
        client.open(base + '/unknown', timeout=3)
    except HTTPError as error:
        assert error.code == 404
        error.close()
    else:
        raise AssertionError('Unknown route did not return 404')
    print('HTTP smoke checks passed: HTML 200, JSON health 200, unknown route 404')


if __name__ == '__main__':
    check()
