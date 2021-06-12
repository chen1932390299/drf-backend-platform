import logging
from rest_framework.views import exception_handler as rest_handler
from rest_framework.response import Response
from . custom_response import CustomResponse
logger = logging.getLogger("day-handler")


def exception_handler(exc, context):
    """
    :param exc: 异常
    :param context: 上下文
    :return: Response object
    """

    response = rest_handler(exc, context)
    context_view = context.get("view", None)
    context_path = context.get('request').path
    context_method = context.get('request').method
    context_ip = context.get('request').META.get("REMOTE_ADDR")

    if response is None:
        logger.error('%s,%s' % (context_view, exc))
        response = Response(
            {'success': False, 'msg': str(exc).replace('\\', ''), "path": context_path, "method": context_method,
             'remote_address': context_ip})
        return response
    if response.status_code == 400:
        response = CustomResponse(data=[], code=response.status_code, status=response.status_code,
                                msg=response.data, success=False)
    if response.status_code == 404:
        response = CustomResponse(data=response.data, code=response.status_code, status=response.status_code,
                                msg='404_Not Found', success=False)
    if response.status_code == 401:
        response = CustomResponse(data=response.data, code=response.status_code, status=response.status_code,
                                msg='401_UNAUTHORIZED', success=False)
    if response.status_code == 403:
        response = CustomResponse(data=response.data, code=response.status_code, status=response.status_code,
                                msg='403_FORBIDDEN ', success=False)
    if response.status_code == 405:
        response = CustomResponse(data=response.data, code=response.status_code, status=response.status_code,
                                msg='405_METHOD_NOT_ALLOWED', success=False)
    if 500 <= response.status_code <= 599:
        response = CustomResponse(data=response.data, code=response.status_code, status=response.status_code,
                                msg='INTERNAL_SERVER_ERROR', success=False)
    return response
