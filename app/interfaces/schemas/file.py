from typing import Optional

from pydantic import BaseModel, Field


class FileReadRequest(BaseModel):
    """读取文件请求结构体"""
    filepath: str = Field(..., description="要读取文件的绝对路径")
    start_line: Optional[int] = Field(default=None, description="(可选)读取的起始行，索引从0开始")
    end_line: Optional[int] = Field(default=None, description="(可选)结束行号、不包含该行")
    sudo: bool = Field(default=False, description="(可选)是否使用 sudo 权限")
    max_length: int = Field(default=10000, description="(可选)要返回内容的最大长度")


class FileWriteRequest(BaseModel):
    """写入文件请求结构体"""
    filepath: str = Field(..., description="要写入文件的绝对路径")
    content: str = Field(..., description="要写入的文本内容")
    append: bool = Field(default=False, description="(可选)是否使用追加模式")
    leading_newline: bool = Field(default=False, description="(可选)是否在内容开头添加空行")
    trailing_newline: bool = Field(default=False, description="(可选)是否在内容结尾添加空行")
    sudo: bool = Field(default=False, description="(可选)是否使用 sudo 权限")
