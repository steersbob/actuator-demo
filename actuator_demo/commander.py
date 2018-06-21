"""
Sends serial commands to the Spark
"""

from functools import partial

from aiohttp import web
from brewblox_devcon_spark import communication
from brewblox_service import brewblox_logger, events

LOGGER = brewblox_logger(__name__)
routes = web.RouteTableDef()


def setup(app: web.Application):
    app.router.add_routes(routes)


def subscribe(app: web.Application, exchange_name: str, routing: str):

    async def _on_event_message(
        app: web.Application,
        subscription: events.EventSubscription,
        routing: str,
        message: dict
    ):
        await send_command(
            app,
            red=message['left_trigger'] * 255,
            green=message['right_trigger'] * 255,
            blue=0
        )

    events.get_listener(app).subscribe(
        exchange_name=exchange_name,
        routing=routing,
        on_message=partial(_on_event_message, app)
    )


async def send_command(app: web.Application, red: int, green: int, blue: int):
    def limit(v):
        return int(min(abs(v), 255))

    cmd = f'{limit(red)} {limit(green)} {limit(blue)}'
    await communication.get_conduit(app).write(cmd)


@routes.post('/command')
async def do_command(request: web.Request) -> web.Response:
    """
    ---
    tags:
    - Actuator
    summary: Send a command
    operationId: actuator.command
    produces:
    - application/json
    parameters:
    -
        in: body
        name: body
        description: command
        required: true
        schema:
            type: object
            properties:
                red:
                    type: int
                    example: 100
                green:
                    type: int
                    example: 100
                blue:
                    type: int
                    example: 100
    """
    args = await request.json()

    await send_command(
        request.app,
        args.get('red', 0),
        args.get('green', 0),
        args.get('blue', 0)
    )
    return web.Response()


@routes.post('/subscribe')
async def add_subscription(request: web.Request) -> web.Response:
    """
    ---
    tags:
    - Actuator
    summary: Add a new event subscription
    operationId: actuator.subscribe
    produces:
    - application/json
    parameters:
    -
        in: body
        name: body
        description: subscription
        required: true
        schema:
            type: object
            properties:
                exchange:
                    type: string
                    example: brewcast
                routing:
                    type: string
                    example: controller.#
    """
    args = await request.json()
    exchange = args['exchange']
    routing = args['routing']

    subscribe(request.app, exchange, routing)
    return web.Response()
