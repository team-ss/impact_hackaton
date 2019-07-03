import asyncio

import pytest
import ujson

from service_api.services import BaseRestClient, RedisCacheManager

HTTPBIN_URL = 'http://httpbin.org'


@pytest.fixture
def base_url_mock(monkeypatch):
    monkeypatch.setattr(BaseRestClient, 'api_url', HTTPBIN_URL)


@pytest.mark.usefixtures('base_url_mock')
async def test_get(test_cli):
    url = 'get'
    headers = {'key': 'value'}
    response = await BaseRestClient.get(url, headers, key='value')
    assert 200 == response.status
    assert 'value' == response.data['headers']['Key']
    assert 'value' == response.data['args']['key']
    await asyncio.sleep(1)  # wait for async cache task
    expected = {
        'data': {'args': {'key': 'value'},
                 'url': 'https://httpbin.org/get?key=value'},
        'status': 200
    }

    cache = await RedisCacheManager.check_cache(f'{HTTPBIN_URL}/{url}?key=value', headers)
    cache = ujson.decode(cache, 'UTF-8')
    assert cache.pop('headers')
    cache['data'].pop('headers')
    cache['data'].pop('origin')
    assert expected == cache
