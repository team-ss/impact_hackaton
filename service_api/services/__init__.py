from dataclasses import dataclass
from urllib.parse import urlencode
from sanic.log import logger

import aiohttp
import aioredis
import ujson

from service_api.domain.decorators import asyncio_task


@dataclass
class ResponseWrapper:
    request_url: str
    headers: dict
    status: int
    data: dict


class RedisCacheManager:
    conn = None

    @classmethod
    async def get_conn(cls, redis_url):
        if not cls.conn:
            cls.conn = await aioredis.create_redis(redis_url)

    @classmethod
    async def close_conn(cls):
        if cls.conn:
            cls.conn.close()
            await cls.conn.wait_closed()

    @classmethod
    async def check_cache(cls, url, headers):
        return await cls.conn.get(cls.__create_key(url, **headers))

    @classmethod
    @asyncio_task
    async def cache_data(cls, url, headers, data, ttl=180):
        key = cls.__create_key(url, **headers)
        json = ujson.encode(data, ensure_ascii=False)
        return await cls.conn.set(key, json, expire=ttl)

    @staticmethod
    def __create_key(url, **headers):
        data = dict(url=url, **headers)
        return hash(frozenset(data))


class BaseRestClient:
    # 0 means that aiohttp will never interrupt connection by itself
    REQUEST_TIMEOUT = 0
    api_url = ''
    __cache_manager = RedisCacheManager

    @classmethod
    async def get(cls, url, headers=None, **kwargs):
        params = urlencode(kwargs, True)
        request_url = f'{cls.api_url}/{url}?{params}'
        cache = await cls.__cache_manager.check_cache(request_url, headers)
        if cache:
            return cache
        else:
            response = await cls.__make_http_request('GET', url, headers, params=params)
            cls.__cache_manager.cache_data(request_url, headers, response.data)
            return response

    @classmethod
    async def post(cls, url, headers=None, data=None):
        return await cls.__make_http_request('POST', url, headers, data=data)

    @classmethod
    async def put(cls, url, headers=None, data=None):
        return await cls.__make_http_request('PUT', url, headers, data=data)

    @classmethod
    async def patch(cls, url, headers=None, data=None):
        return await cls.__make_http_request('PATCH', url, headers, data=data)

    @classmethod
    async def delete(cls, url, headers=None, **kwargs):
        params = urlencode(kwargs, True)
        return await cls.__make_http_request('DELETE', url, headers, params=params)

    @classmethod
    async def __make_http_request(cls, method, url, headers, params=None, data=None):
        request_url = f'{cls.api_url}/{url}?{params}'
        async with aiohttp.ClientSession() as session:
            logger.debug(f'Sending {method} request to {url}, headers: {headers}')
            async with session.request(method=method, url=request_url, data=data, headers=headers,
                                       timeout=cls.REQUEST_TIMEOUT) as response:
                logger.debug(f'Got response from {request_url}, status {response.status}')
                try:
                    resp_data = await response.json()
                # type: ignore
                except aiohttp.ContentTypeError:
                    return ResponseWrapper(request_url=request_url, headers=dict(response.headers),
                                           status=response.status, data=response.content)
                else:
                    return ResponseWrapper(request_url=request_url, headers=dict(response.headers),
                                           status=response.status,
                                           data=resp_data)
