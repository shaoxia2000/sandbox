from fastapi import APIRouter, Depends

from app.interfaces.schemas.base import Response
from app.interfaces.schemas.file import FileReadRequest, FileWriteRequest, FileReplaceRequest, FileSearchRequest, \
    FileFindRequest
from app.interfaces.service_dependencies import get_file_service
from app.models.file import FileReadResult, FileWriteResult, FileReplaceResult, FileSearchResult
from app.services.file import FileService

router = APIRouter(prefix="/file", tags=["File模块"])


@router.post(
    path="/read-file",
    response_model=Response[FileReadResult],
)
async def read_file(
        request: FileReadRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileReadResult]:
    """根据传递的数据读取沙箱中的文件内容"""
    result = await file_service.read_file(
        filepath=request.filepath,
        start_line=request.start_line,
        end_line=request.end_line,
        sudo=request.sudo,
        max_length=request.max_length,
    )
    return Response.success(
        msg="文件内容读取成功",
        data=result,
    )


@router.post(
    path="/write-file",
    response_model=Response[FileWriteResult],
)
async def write_file(
        request: FileWriteRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileWriteResult]:
    """根据传递的数据向指定文件写入内容"""
    result = await file_service.write_file(
        filepath=request.filepath,
        content=request.content,
        append=request.append,
        leading_newline=request.leading_newline,
        trailing_newline=request.trailing_newline,
        sudo=request.sudo,
    )
    return Response.success(msg="文件内容写入成功", data=result)


@router.post(
    path="/replace-in-file",
    response_model=Response[FileReplaceResult],
)
async def replace_in_file(
        request: FileReplaceRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileReplaceResult]:
    """根据传递的数据替换文件内的部分内容"""
    result = await file_service.replace_in_file(
        filepath=request.filepath,
        old_str=request.old_str,
        new_str=request.new_str,
        sudo=request.sudo,
    )
    return Response.success(
        msg=f"文件内容替换完成, 已替换{result.replaced_count}处内容",
        data=result,
    )


@router.post(
    path="/search-in-file",
    response_model=Response[FileSearchResult],
)
async def search_in_file(
        request: FileSearchRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileSearchResult]:
    """根据传递的数据检索指定文件的内容"""
    result = await file_service.search_in_file(
        filepath=request.filepath,
        regex=request.regex,
        sudo=request.sudo,
    )
    return Response.success(
        msg=f"文件内容搜索完成, 找到{len(result.matches)}处匹配内容",
        data=result,
    )


@router.post(
    path="/find-files",
    response_model=Response[FileFindRequest],
)
async def find_files(
        request: FileFindRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileFindRequest]:
    """根据传递的文件夹+glob文件规则查找文件列表"""
    result = await file_service.find_files(
        dir_path=request.dir_path,
        glob_pattern=request.glob_pattern,
    )
    return Response.success(
        msg=f"查找完毕, 检索到{len(result.files)}个文件",
        data=result,
    )
