from argrelay.interp_plugin.AbstractInterpFactory import AbstractInterpFactory
from argrelay.interp_plugin.NamedNoopInterp import NamedNoopInterp
from argrelay.runtime_context.InterpContext import InterpContext


class NamedNoopInterpFactory(AbstractInterpFactory):

    def __init__(self, config_dict: dict):
        super().__init__(config_dict)

    def create_interp(self, interp_ctx: InterpContext) -> NamedNoopInterp:
        return NamedNoopInterp(interp_ctx, self.config_dict)