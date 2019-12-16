from flask import Flask

from mbconfig import MBConfig
from subscriber import bp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(MBCONFIG=MBConfig(path=app.instance_path))
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(bp)

    return app


flask_app = create_app()
