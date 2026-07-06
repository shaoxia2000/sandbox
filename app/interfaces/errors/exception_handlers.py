import logging

from fastapi import FastAPI, Request
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.interfaces.errors.exceptions import AppException
from app.interfaces.schemas.base import Response

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """处理MoocManus沙箱项目中所有的异常并进行统一处理, 涵盖：自定义业务状态异常、http异常、通用异常"""

    @app.exception_handler(AppException)
    async def app_exception_handler(req: Request, e: AppException) -> JSONResponse:
        """处理MoocManus业务异常"""
        logger.error(f"AppException: {e.msg}")
        return JSONResponse(
            status_code=e.status_code,
            content=Response(
                code=e.status_code,
                msg=e.msg,
                data={}
            ).model_dump()
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(req: Request, e: HTTPException) -> JSONResponse:
        """处理FastAPI中抛出的http异常"""
        logger.error(f"HTTPException: {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content=Response(
                code=e.status_code,
                msg=str(e.detail),
                data={}
            ).model_dump()
        )

    @app.exception_handler(Exception)
    async def exception_handler(req: Request, e: Exception) -> JSONResponse:
        """处理MoocManus沙箱项目中抛出的未定义任意异常，将状态码统一设置为500"""
        logger.error(f"Exception: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=Response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="服务器出现异常，请稍后重试",
                data={}
            ).model_dump()
        )
