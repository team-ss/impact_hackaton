import json


async def test_googleapiclient(test_cli):
    body = {'origin': 'London', 'destination': 'Heathrow'}
    response = await test_cli.post('/route', data=json.dumps(body))
    assert 200 == response.status
