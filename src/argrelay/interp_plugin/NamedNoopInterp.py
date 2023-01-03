from argrelay.interp_plugin.AbstractInterp import AbstractInterp
from argrelay.runtime_context.InterpContext import InterpContext


class NamedNoopInterp(AbstractInterp):
    """
    Interpreter which does nothing

    Actually, it:
    *   stops processing of the command line on itself (as `next_interp` returns `None`
    *   names itself based on config
    """

    instance_name: str

    def __init__(self, interp_ctx: InterpContext, config_dict: dict):
        super().__init__(interp_ctx, config_dict)
        self.instance_name = config_dict["instance_name"]

    def try_iterate(self) -> int:
        return 0

    def next_interp(self) -> "AbstractInterp":
        return None