from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

import aiohttp
import aioredis
import ujson
from aioredis.commands import Redis
from sanic.log import logger

from service_api.domain.decorators import asyncio_task


@dataclass
class ResponseWrapper:
    request_url: str
    headers: dict
    status: int
    data: dict

    @property
    def ok(self):
        return self.status // 200 == 1


class RedisCacheManager:
    conn: Redis = None

    @classmethod
    async def get_conn(cls, redis_url: str) -> None:
        if not cls.conn:
            cls.conn = await aioredis.create_redis(redis_url)

    @classmethod
    async def close_conn(cls):
        if cls.conn:
            cls.conn.close()
            await cls.conn.wait_closed()

    @classmethod
    async def check_cache(cls, url: str, headers: Optional[dict] = None) -> Optional[bytes]:
        return await cls.conn.get(cls.__create_key(url, headers))

    @classmethod
    @asyncio_task
    async def cache_data(cls, url: str, response: ResponseWrapper, request_headers: Optional[dict],
                         ttl: int = 180) -> int:
        key = cls.__create_key(url, request_headers)
        hash_data = {
            'status': response.status,
            'headers': response.headers,
            'data': response.data
        }
        json = ujson.dumps(hash_data, ensure_ascii=False)
        return await cls.conn.set(key, json, expire=ttl)

    @staticmethod
    def __create_key(url: str, headers: Optional[dict] = None) -> int:
        data: dict = headers or {}
        data['url'] = url
        return hash(frozenset(data))


class BaseRestClient:
    # 0 means that aiohttp will never interrupt connection by itself
    REQUEST_TIMEOUT = 0
    api_url = ''
    __cache_manager = RedisCacheManager

    @classmethod
    async def get(cls, url: str, headers: Optional[dict] = None, **kwargs) -> ResponseWrapper:
        params = urlencode(kwargs, True)
        request_url = f'{cls.api_url}/{url}?{params}'
        cache = await cls.__cache_manager.check_cache(request_url, headers)
        if cache:
            cache_data = ujson.loads(cache)
            return ResponseWrapper(request_url=request_url, headers=cache_data['headers'], status=cache_data['status'],
                                   data=cache_data['data'])
        else:
            response = await cls.__make_http_request('GET', url, headers, params=params)
            if response.ok:
                await cls.__cache_manager.cache_data(request_url, response, request_headers=headers)
            return response

    @classmethod
    async def post(cls, url: str, headers: Optional[dict] = None, data: Optional[dict] = None) -> ResponseWrapper:
        return await cls.__make_http_request('POST', url, headers, data=data)

    @classmethod
    async def put(cls, url: str, headers: Optional[dict] = None, data: Optional[dict] = None) -> ResponseWrapper:
        return await cls.__make_http_request('PUT', url, headers, data=data)

    @classmethod
    async def patch(cls, url: str, headers: Optional[dict] = None, data: Optional[dict] = None) -> ResponseWrapper:
        return await cls.__make_http_request('PATCH', url, headers, data=data)

    @classmethod
    async def delete(cls, url: str, headers: Optional[dict] = None, **kwargs) -> ResponseWrapper:
        params = urlencode(kwargs, True)
        return await cls.__make_http_request('DELETE', url, headers, params=params)

    @classmethod
    async def __make_http_request(cls, method: str, url: str, headers: Optional[dict] = None,
                                  params: Optional[str] = None, data: Optional[dict] = None) -> ResponseWrapper:
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
                                           status=response.status, data=dict(error=response.text))
                else:
                    return ResponseWrapper(request_url=request_url, headers=dict(response.headers),
                                           status=response.status,
                                           data=resp_data)
