from argrelay.enum_desc.GlobalArgType import GlobalArgType
from argrelay.enum_desc.ReservedArgType import ReservedArgType
from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.enum_desc.SpecialFunc import SpecialFunc
from argrelay.plugin_delegator.HelpDelegator import HelpDelegator
from argrelay.plugin_loader.AbstractLoader import AbstractLoader
from argrelay.runtime_data.StaticData import StaticData
from argrelay.schema_config_interp.DataEnvelopeSchema import envelope_id_, instance_data_
from argrelay.schema_config_interp.FunctionEnvelopeInstanceDataSchema import (
    delegator_plugin_instance_id_,
    search_control_list_,
)


class HelpLoader(AbstractLoader):

    def update_static_data(
        self,
        static_data: StaticData,
    ) -> StaticData:
        data_envelopes = static_data.data_envelopes

        given_function_envelope = {
            envelope_id_: SpecialFunc.help_func.name,
            instance_data_: {
                delegator_plugin_instance_id_: HelpDelegator.__name__,
                search_control_list_: [
                ],
            },
            ReservedArgType.EnvelopeClass.name: ReservedEnvelopeClass.ClassFunction.name,
            ReservedArgType.HelpHint.name: "List defined function matching search criteria with their help hints",
            GlobalArgType.FunctionCategory.name: "internal",
            GlobalArgType.ActionType.name: "help",
            GlobalArgType.ObjectSelector.name: "func",
        }
        data_envelopes.append(given_function_envelope)

        return static_data
