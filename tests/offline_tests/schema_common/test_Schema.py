from unittest import TestCase

from argrelay.relay_demo.DemoInterpConfigSchema import demo_interp_config_desc
from argrelay.relay_demo.GitRepoLoaderConfigSchema import git_repo_loader_config_desc
from argrelay.schema_config_core_client.ClientConfigSchema import client_config_desc
from argrelay.schema_config_core_client.ConnectionConfigSchema import connection_config_desc
from argrelay.schema_config_core_server.FirstArgInterpFactorySchema import first_arg_interp_config_desc
from argrelay.schema_config_core_server.MongoClientConfigSchema import mongo_client_config_desc
from argrelay.schema_config_core_server.MongoConfigSchema import mongo_config_desc
from argrelay.schema_config_core_server.MongoServerConfigSchema import mongo_server_config_desc
from argrelay.schema_config_core_server.ServerConfigSchema import server_config_desc
from argrelay.schema_config_core_server.StaticDataSchema import static_data_desc
from argrelay.schema_config_interp.DataEnvelopeSchema import data_envelope_desc
from argrelay.schema_config_interp.EnvelopeClassQuerySchema import envelope_class_query_desc
from argrelay.schema_config_interp.FuncArgsInterpConfigSchema import func_args_interp_config_desc
from argrelay.schema_config_interp.FunctionEnvelopeInstanceDataSchema import function_envelope_instance_data_desc
from argrelay.schema_config_plugin.PluginEntrySchema import plugin_entry_desc
from argrelay.schema_request.RequestContextSchema import request_context_desc
from argrelay.schema_response.ArgValuesSchema import arg_values_desc
from argrelay.schema_response.AssignedValueSchema import assigned_value_desc
from argrelay.schema_response.EnvelopeContainerSchema import envelope_container_desc
from argrelay.schema_response.InterpResultSchema import interp_result_desc
from argrelay.schema_response.InvocationInputSchema import invocation_input_desc
from argrelay.test_helper import line_no


class ThisTestCase(TestCase):

    def test_type_desc_example_is_loadable_and_dumpable(self):
        test_cases = [
            (line_no(), request_context_desc),
            (line_no(), invocation_input_desc),
            (line_no(), plugin_entry_desc),
            (line_no(), demo_interp_config_desc),
            (line_no(), git_repo_loader_config_desc),
            (line_no(), client_config_desc),
            (line_no(), connection_config_desc),
            (line_no(), first_arg_interp_config_desc),
            (line_no(), mongo_client_config_desc),
            (line_no(), mongo_config_desc),
            (line_no(), mongo_server_config_desc),
            (line_no(), server_config_desc),
            (line_no(), static_data_desc),
            (line_no(), data_envelope_desc),
            (line_no(), envelope_class_query_desc),
            (line_no(), function_envelope_instance_data_desc),
            (line_no(), func_args_interp_config_desc),
            (line_no(), arg_values_desc),
            (line_no(), interp_result_desc),
            (line_no(), assigned_value_desc),
            (line_no(), envelope_container_desc),
        ]
        for test_case in test_cases:
            with self.subTest(test_case):
                (line_number, type_desc) = test_case
                loaded_obj = type_desc.dict_schema.load(type_desc.dict_example)
                dumped_dict = type_desc.dict_schema.dump(loaded_obj)
                # Compare via JSON strings:
                orig_json = type_desc.dict_schema.dumps(type_desc.dict_example, sort_keys = True)
                dumped_json = type_desc.dict_schema.dumps(dumped_dict, sort_keys = True)
                self.maxDiff = None
                self.assertEqual(
                    orig_json,
                    dumped_json,
                )
