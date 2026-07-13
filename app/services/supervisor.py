"""
1.Supervisor启动后通过一个unix套接字文件来实现通信(rpc协议)
2.连接这个通信文件， /tmp/supervisor.sock (通过python提供的一个库xml-rpc连接)
3.xml-rpc它的连接必须是网络协议，而我们这里是本地文件，所以得做相应的转换
4.使用某种方式进行转换，让xml-rpc实现链接supervisor.sock
5.连接之后我们就可以调用rpc对应的方法, 例如: getAllProcessInfo()
"""
import asyncio
import logging
import socket
import xmlrpc

import http
from typing import List, Any

from app.interfaces.errors.exceptions import BadRequestException, AppException
from app.models.supervisor import ProcessInfo

logger = logging.getLogger(__name__)


class UnixStreamHTTPConnection(http.client.HTTPConnection):
    """基于Unix流的HTTP连接处理器"""

    def __init__(self, host: str, socket_path: str, timeout=None) -> None:
        """构造函数, 完成连接处理器初始化"""
        http.client.HTTPConnection.__init__(self, host, timeout=timeout)
        self.socket_path = socket_path

    def connect(self) -> None:
        """重写链接方法，欺骗xml-rpc库让其觉得自己正在进行网络连接"""
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)


class UnixStreamTransport(xmlrpc.client.Transport):
    """基于Unix流传输层的适配器/转换器"""

    def __init__(self, socket_path: str) -> None:
        """构造函数，完成传输适配器的初始化"""
        xmlrpc.client.Transport.__init__(self)
        self.socket_path = socket_path

    def make_connection(self, host) -> http.client.HTTPConnection:
        return UnixStreamHTTPConnection(host, self.socket_path)


class SupervisorService:
    """Supervisor服务"""

    def __init__(self) -> None:
        """构造函数，完成supervisor服务链接"""
        self.rpc_url = "/tmp/supervisor.sock"
        self._connect_rpc()

    def _connect_rpc(self):
        """使用python的xml-rpc客户端链接一个本地sock文件实现连接rpc服务"""
        try:
            self.server = xmlrpc.client.ServerProxy(
                "http://localhost",
                transport=UnixStreamTransport(self.rpc_url),
            )
        except Exception as e:
            logger.error(f"连接supervisor服务失败: {str(e)}")
            raise BadRequestException(f"连接supervisor服务失败: {str(e)}")

    @classmethod
    async def _call_rpc(cls, method, *args) -> Any:
        """根据传递的方法+参数 调用rpc方法"""
        try:
            return await asyncio.to_thread(method, *args)
        except Exception as e:
            logger.error(f"RPC方法调用失败: {str(e)}")
            raise BadRequestException(f"RPC方法调用失败: {str(e)}")

    async def get_all_processes(self) -> List[ProcessInfo]:
        """获取当前supervisor管理的所有进程信息"""
        try:
           processes = await self._call_rpc(self.server.supervisor.getAllProcessInfo)
           return [ProcessInfo(**process) for process in processes]
        except Exception as e:
            logger.error(f"获取进程信息失败: {str(e)}")
            raise AppException(f"获取进程信息失败: {str(e)}")
