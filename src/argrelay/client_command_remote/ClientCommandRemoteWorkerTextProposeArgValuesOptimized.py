import json
import os
import socket

from argrelay.client_command_remote.ClientCommandRemoteAbstract import ClientCommandRemoteAbstract
from argrelay.client_pipeline.BytesSrcAbstract import BytesSrcAbstract
from argrelay.enum_desc.ProcRole import ProcRole
from argrelay.enum_desc.ServerAction import ServerAction
from argrelay.misc_helper_common.ElapsedTime import ElapsedTime
from argrelay.runtime_data.ConnectionConfig import ConnectionConfig
from argrelay.server_spec.CallContext import CallContext


class ClientCommandRemoteWorkerTextProposeArgValuesOptimized(ClientCommandRemoteAbstract):
    """
    This class optimizes what can otherwise be done via generic `ClientCommandRemoteWorkerJson`.

    See `completion_perf_notes.md`.

    Importing many packages including `marshmallow` slows down startup and responses on `Tab` requests.

    Performance is not critical for other client commands
    (e.g. `ServerAction.DescribeLineArgs` or `ServerAction.RelayLineArgs`),
    but it is critical for `Tab` (`ServerAction.ProposeArgValues`).

    Because `Tab`-completion is latency-sensitive, `ServerAction.ProposeArgValues` uses this specialized implementation.
    The drawback is that it also requires special maintenance/testing.
    """

    # TODO: Provide test coverage for this special implementation.
    #       Write mocked test to cover internal logic like function `recvall` below.

    def __init__(
        self,
        call_ctx: CallContext,
        proc_role: ProcRole,
        connection_config: ConnectionConfig,
        bytes_src: BytesSrcAbstract,
    ):
        super().__init__(
            call_ctx,
            proc_role,
        )
        self.connection_config: ConnectionConfig = connection_config
        self.bytes_src: BytesSrcAbstract = bytes_src
        self.server_path: str = ServerAction.ProposeArgValues.value

    def _execute_remotely(
        self,
    ):

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        ) as s:
            self.execute_command_with_socket(s)

    def execute_command_with_socket(
        self,
        s,
    ):
        s.connect((
            self.connection_config.server_host_name,
            self.connection_config.server_port_number,
        ))

        request_body_str = (f"""\
{{
    "server_action": "{self.call_ctx.server_action.name}",
    "command_line": {json.dumps(self.call_ctx.command_line)},
    "cursor_cpos": {self.call_ctx.cursor_cpos},
    "comp_scope": "{self.call_ctx.comp_scope.name}",
    "client_pid": "{os.getpid()}",
    "is_debug_enabled": "{'true' if self.call_ctx.is_debug_enabled else 'false'}"
}}
""")
        request_body_len = len(request_body_str.encode())

        request_str = (f"""\
POST {self.server_path} HTTP/1.1\r
Content-Type: application/json\r
Content-Length: {request_body_len}\r
Connection: close\r
\r
{request_body_str}
""")
        ElapsedTime.measure("before_request")

        s.sendall(request_str.encode())
        response_str = self.recvall(s).decode()

        ElapsedTime.measure("after_request")

        # First line, second space-delimited substring:
        # HTTP/1.1 200 OK\r\n
        response_status_line = response_str[:response_str.find("\r")]
        first_space_cpos = response_status_line.find(" ")
        response_status_code = int(
            response_status_line[first_space_cpos + 1:first_space_cpos + 1 + 3]
        )
        # Content after headers (after empty line):
        content_cpos = response_str.find("\r\n\r\n") + 4
        if content_cpos < len(response_str):
            response_body_str = response_str[content_cpos:]
        else:
            response_body_str = ""

        ElapsedTime.measure("after_deserialization")

        try:
            if response_status_code == 200:
                self.bytes_src.accept_bytes(response_body_str.encode())
            else:
                self.raise_error(response_status_code)
        finally:
            ElapsedTime.measure("after_handle_response")

    # noinspection SpellCheckingInspection
    @staticmethod
    def recvall(s):
        bytes_parts = []
        while True:
            bytes_part = s.recv(1000)
            if not bytes_part:
                break
            bytes_parts.append(bytes_part)
        return b"".join(bytes_parts)
