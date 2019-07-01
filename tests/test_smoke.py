async def test_smoke(test_cli):
    resp = await test_cli.get('/smoke')
    assert 200 == resp.status
