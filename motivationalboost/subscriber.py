from flask import (
    Blueprint, request, current_app, make_response
)

from . import request_handler

bp = Blueprint('subscriber', __name__)


# Handle POST to the /response endpoint that indicate new survey responses are available
@bp.route('/response', methods=['POST'])
def event_subscriber():
    current_app.logger.info(str(request.form))
    response_id = request.form['ResponseID']

    try:
        handler = request_handler.RequestHandler(config=current_app.config['MBCONFIG'], response_id=response_id)
        handler.handle_request()
    except KeyError as ke:
        current_app.logger.exception(str(ke))

    # return successfully
    return make_response('', 200)
