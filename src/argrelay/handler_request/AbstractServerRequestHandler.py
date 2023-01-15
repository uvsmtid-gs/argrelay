from argrelay.meta_data.RunMode import RunMode
from argrelay.relay_server.LocalServer import LocalServer
from argrelay.runtime_context.InputContext import InputContext
from argrelay.runtime_context.InterpContext import InterpContext
from argrelay.runtime_context.ParsedContext import ParsedContext
from argrelay.runtime_context.RequestContext import RequestContext


class AbstractServerRequestHandler:
    local_server: LocalServer
    interp_ctx: InterpContext

    def __init__(
        self,
        local_server: LocalServer,
    ):
        self.local_server = local_server

    def handle_request(self, input_ctx: InputContext) -> dict:
        raise NotImplementedError

    @staticmethod
    def create_input_ctx(request_ctx: RequestContext, run_mode: RunMode):
        input_ctx = InputContext.from_request_context(
            request_ctx,
            run_mode = run_mode,
            comp_key = str(0),
        )
        return input_ctx

    def interpret_command(self, local_server: LocalServer, input_ctx: InputContext):
        parsed_ctx = ParsedContext.from_instance(input_ctx)
        # TODO: Split server_config and static_data (both top level, not config including data):
        self.interp_ctx = InterpContext(
            parsed_ctx,
            local_server.server_config.static_data,
            local_server.server_config.interp_factories,
            local_server.server_config.action_invocators,
            local_server.get_mongo_database(),
        )
        self.interp_ctx.interpret_command()
        self.interp_ctx.print_debug()