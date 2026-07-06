import os.path

from fastapi import APIRouter, Depends

from app.interfaces.schemas.base import Response
from app.interfaces.schemas.shell import ExecCommandRequest
from app.interfaces.service_dependencies import get_shell_service
from app.models.shell import ShellExecResult
from app.services.shell import ShellService

router = APIRouter(prefix="/shell", tags=["Shell模块"])


@router.post(
    path="/exec-command",
    response_model=Response[ShellExecResult],
)
async def exec_command(
        request: ExecCommandRequest,
        shell_service: ShellService = Depends(get_shell_service),
) -> Response[ShellExecResult]:
    """在指定的Shell会话中运行命令"""
    # 1.判断下是否传递了session_id, 如果不存在则新建一个session_id
    session_id = request.session_id or shell_service.create_session_id()
    # 2.判断下是否传递了执行目录, 如果未传递则使用根目录作为执行路径
    exec_dir = request.exec_dir or os.path.expanduser("~")  # 在不同的系统下获取的根目录路径是不一样的
    # 3.调用服务执行命令获取结果
    result = await shell_service.exec_command(
        session_id=session_id,
        exec_dir=exec_dir,
        command=request.command,
    )
    return Response.success(data=result)
