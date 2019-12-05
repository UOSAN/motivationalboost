from flask import (
    Blueprint, request, current_app, make_response
)

from .request_handler import RequestHandler

bp = Blueprint('subscriber', __name__)


# Handle POST to the /response endpoint that contains the required survey output
@bp.route('/response', methods=['POST'])
def event_subscriber():
    if request.is_json:
        survey_output = request.get_json()
        current_app.logger.info(f'New survey response received:\n{str(survey_output)}\n')

        try:
            handler = RequestHandler(config=current_app.config['MBCONFIG'], survey_output=survey_output)
            handler.handle_request()
        except KeyError as ke:
            current_app.logger.exception(str(ke))
    else:
        current_app.logger.info(f'POST request:\n{request.data}\n')
        return make_response('', 400)

    # return successfully
    return make_response('', 200)
