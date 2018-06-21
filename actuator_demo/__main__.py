"""
Entrypoint for the actuator demo application
"""

from brewblox_devcon_spark import communication
from brewblox_service import brewblox_logger, events, service

from actuator_demo import commander

LOGGER = brewblox_logger(__name__)


def create_parser(default_name='lamp'):
    parser = service.create_parser(default_name=default_name)
    parser.add_argument('--device-port',
                        help='Spark device port. Automatically determined if not set. [%(default)s]')
    parser.add_argument('--device-id',
                        help='Spark serial number. Any spark is valid if not set. '
                        'This will be ignored if --device-port is specified. [%(default)s]')
    parser.add_argument('--broadcast-exchange',
                        help='Eventbus exchange to which controller state should be broadcasted. [%(default)s]',
                        default='brewcast')
    return parser


def main():
    app = service.create_app(parser=create_parser())

    events.setup(app)
    communication.setup(app)
    commander.setup(app)

    commander.subscribe(
        app,
        app['config']['broadcast_exchange'],
        routing='game.#'
    )

    service.furnish(app)
    service.run(app)


if __name__ == '__main__':
    main()
