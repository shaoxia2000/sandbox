from typing import Optional, List

from pydantic import BaseModel, Field


class FileReadResult(BaseModel):
    """文件读取结果"""
    file_path: str = Field(..., description="要读取的文件路径")
    content: str = Field(..., description="读取的文件内容")


class FileWriteResult(BaseModel):
    """文件写入结果"""
    filepath: str = Field(..., description="要写入的文件绝对路径")
    bytes_written: Optional[int] = Field(default=None, description="写入文件内容的字节数")


class FileReplaceResult(BaseModel):
    """文件内容替换结果模型"""
    filepath: str = Field(..., description="要替换内容的文件绝对路径")
    replaced_count: int = Field(default=0, description="替换内容的次数")


class FileSearchResult(BaseModel):
    """文件搜索结果"""
    filepath: str = Field(..., description="要搜索内容的文件绝对路径")
    matches: List[str] = Field(default_factory=list, description="匹配内容列表")
    line_numbers: List[int] = Field(default_factory=list, description="匹配的行号列表")


class FileFindResult(BaseModel):
    """文件查找结果"""
    dir_path: str = Field(..., description="搜索的目录绝对路径")
    files: List[str] = Field(default_factory=list, description="检索到的文件列表")
