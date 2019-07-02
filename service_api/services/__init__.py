from dataclasses import dataclass

import aiohttp
from urllib.parse import urlencode


@dataclass
class ResponseWrapper:
    request_url: str
    headers: dict
    status: int
    data: dict


class BaseRestClient:
    # 0 means that aiohttp will never interrupt connection by itself
    REQUEST_TIMEOUT = 0
    api_url = ''

    @classmethod
    async def get(cls, url, headers=None, **kwargs):
        params = urlencode(kwargs, True)
        return await cls.__make_http_request('GET', url, headers, params=params)

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
        request_url = f'{url}/{url}?{params}'
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=request_url, data=data, headers=headers,
                                       timeout=cls.REQUEST_TIMEOUT) as response:
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
