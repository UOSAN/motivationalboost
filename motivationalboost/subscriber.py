from flask import (
    Blueprint, request, current_app, make_response
)

from . import request_handler

bp = Blueprint('subscriber', __name__)


# Handle POST to the /response endpoint that indicate new survey responses are available
@bp.route('/response', methods=['POST'])
def event_subscriber():
    survey_id = request.form['SurveyID']
    response_id = request.form['ResponseID']

    handler = request_handler.RequestHandler(config=current_app.config['config'], response_id=response_id)
    handler.handle_request()

    # return successfully
    return make_response('', 200)
