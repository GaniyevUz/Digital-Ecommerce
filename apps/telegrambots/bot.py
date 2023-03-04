from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/bot/{token}/')
async def hello(request):
    token = request.match_info['token']
    return web.Response(text=f"Hello, {token}")


@routes.post('/updates')
async def hello(request):
    token = request.match_info['token']
    return web.Response(text=f"Hello, {token}")


app = web.Application()
app.add_routes(routes)
web.run_app(app)
