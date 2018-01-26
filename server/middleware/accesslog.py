import structlog
import hug

import common.logging


def setup_access_log(app: hug.API, logger: common.logging.Logger):
    @hug.request_middleware(api=app)
    def process_request(request: hug.Request, response: hug.Response):
        """Logs the basic endpoint requested"""
        logger.info('incoming request',
                    remote_addr=request.remote_addr,
                    method=request.method,
                    uri=request.relative_uri,
                    content_type=request.content_type,
                    user_agent=request.user_agent)

    @hug.response_middleware(api=app)
    def process_response(request: hug.Request, response: hug.Response, resource):
        """Logs the basic data returned by the API"""
        data_len = len(response.data) if response.data is not None else None
        logger.info('generated response',
                    remote_addr=request.remote_addr,
                    method=request.method,
                    uri=request.relative_uri,
                    status=response.status,
                    size=data_len,
                    content_type=response.content_type,
                    user_agent=request.user_agent)
