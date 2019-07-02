import pytest
import asyncio

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
    await asyncio.sleep(2)  # wait for async cache task
    assert await RedisCacheManager.check_cache(f'{HTTPBIN_URL}/{url}?key=value', headers) is not None
