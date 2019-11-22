from flask import Flask

from . import mbconfig


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping({'MBCONFIG', mbconfig.MBConfig()})
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import subscriber
    app.register_blueprint(subscriber.bp)

    return app
