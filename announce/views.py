import logging

logger = logging.getLogger('bellman.views')

from django.http import HttpResponse, HttpResponseBadRequest  # JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from bellman import Bellman
# Create your views here.


def check_token_safe(token):
    return token == settings.SLACK_TOKEN


@csrf_exempt
def announce(request):
    logger.debug("---------------------------------------")
    # default empty text field will be ignored by slack

    # security check
    if request.method == 'POST' and check_token_safe(request.POST['token']):

        logger.debug('POST from northhq slack')
        logger.debug(request.POST)
        args = request.POST['text'].split()
        logger.debug('args:', args)
        num_of_args = len(args)
        logger.debug('num_of_args:', num_of_args)
        logger.debug("---------------------------------------")

        # check that POST has the correct form?

        app = Bellman(
            text=request.POST['text'],
            user_name=request.POST['user_name'],
            user_id=request.POST['user_id'])

        app.execute()

        return HttpResponse(app.get_response())

    elif request.method != 'POST':
        return HttpResponseBadRequest('Did not receive an HTTP POST.')
    elif not check_token_safe(request.POST['token']):
        return HttpResponseBadRequest('Received an invalid token.')
    else:
        HttpResponseBadRequest('Not sure how to handle this request.')
