from argrelay.plugin_interp.AbstractInterpFactory import AbstractInterpFactory
from argrelay.plugin_interp.GenericInterp import GenericInterp
from argrelay.runtime_context.InterpContext import InterpContext
from argrelay.schema_config_interp.EnvelopeClassQuerySchema import keys_to_types_list_
from argrelay.schema_config_interp.GenericInterpConfigSchema import generic_interp_config_desc, function_query_


class GenericInterpFactory(AbstractInterpFactory):

    def __init__(self, config_dict: dict):
        super().__init__(config_dict)
        generic_interp_config_desc.dict_schema.validate(config_dict)

    def create_interp(self, interp_ctx: InterpContext) -> GenericInterp:
        raise NotImplementedError

    def validate_loaded_data(self, static_data: "StaticData"):
        self._validate_function_envelopes_have_unique_coordinates(static_data)

    def _validate_function_envelopes_have_unique_coordinates(self, static_data: "StaticData"):
        """
        Verify that all arg types listed to query functions uniquely identify all function with such arg types

        Otherwise, functions which do not have unque coordinates with listed arg types will not be invokable.

        * Find all envelopes of `ReservedEnvelopeClass.ClassFunction`.
        * Take those of them which have all arg types listed in plugin config.
        * Make sure all arg values (ordered by arg type) have unique tuple.
        """

        types_list = GenericInterp.list_to_dict(self.config_dict[function_query_][keys_to_types_list_]).values()

        all_typed_values_lists = []
        for data_envelope in static_data.data_envelopes:

            all_types_exist = True
            typed_values_list = []
            for type_name in types_list:
                if type_name not in data_envelope:
                    all_types_exist = False
                    break
                else:
                    typed_values_list.append(data_envelope[type_name])

            if all_types_exist:
                assert typed_values_list not in all_typed_values_lists
                all_typed_values_lists.append(typed_values_list)
            else:
                continue
