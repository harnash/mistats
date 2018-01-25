import structlog
import hug


class AccessLogMiddleware(object):
    def __init__(self):
        self.logger = structlog.get_logger('access_log')

    def process_request(self, request: hug.Request, response: hug.Response):
        """Logs the basic endpoint requested"""
        self.logger.info('incoming request',
                         remote_addr=request.remote_addr,
                         method=request.method,
                         uri=request.relative_uri,
                         content_type=request.content_type,
                         user_agent=request.user_agent)

    def process_response(self, request: hug.Request, response: hug.Response, resource):
        """Logs the basic data returned by the API"""
        self.logger.info('generated response',
                         remote_addr=request.remote_addr,
                         method=request.method,
                         uri=request.relative_uri,
                         status=response.status,
                         size=len(response.data),
                         content_type=response.content_type,
                         user_agent=request.user_agent)
