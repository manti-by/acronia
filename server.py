from json import JSONDecodeError

from aiohttp import web
from aiohttp_apispec import docs, request_schema, setup_aiohttp_apispec
from marshmallow import ValidationError

from message import send_message_to_all, send_message
from schemas import MessageSchema

routes = web.RouteTableDef()


@docs(
   tags=["telegram"],
   summary="Send message API",
   description="This end-point sends message to telegram bot user/users",
)
@request_schema(MessageSchema())
@routes.post("/")
async def index_post(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except JSONDecodeError:
        return web.json_response({"result": "Request data is invalid"})
    try:
        schema = MessageSchema()
        data = schema.load(payload)
    except ValidationError as e:
        return web.json_response({"result": "Validation Error", "error": e.messages})

    if data.get("chat_id"):
        await send_message(data.get("chat_id"), data.get("message"))
    else:
        await send_message_to_all(data.get("message"))
    return web.json_response({"result": "OK"})


@docs(
   tags=["telegram"],
   summary="Get status",
   description="Return status of the server",
)
@routes.get("/")
async def index_get(request: web.Request) -> web.Response:
    return web.json_response({"result": "OK"})


if __name__ == "__main__":
    app = web.Application()
    setup_aiohttp_apispec(
        app=app, title="Acronia Bot documentation", version="v1.0",
        url="/api/docs/swagger.json", swagger_path="/api/docs",
    )
    app.add_routes(routes)
    web.run_app(app, port=5000)
