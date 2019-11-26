from logging.config import dictConfig

from flask import Flask

from .mbconfig import MBConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(MBCONFIG=MBConfig())
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from .subscriber import bp
    app.register_blueprint(bp)

    return app


flask_app = create_app()
