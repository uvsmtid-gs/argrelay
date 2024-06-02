from __future__ import annotations

from argrelay.client_command_local.AbstractLocalClientCommand import AbstractLocalClientCommand
from argrelay.composite_tree.CompositeForestSchema import tree_roots_
from argrelay.composite_tree.CompositeNodeSchema import node_type_, plugin_instance_id_, sub_tree_
from argrelay.composite_tree.CompositeNodeType import CompositeNodeType
from argrelay.enum_desc.CompType import CompType
from argrelay.plugin_interp.FirstArgInterpFactory import (
    FirstArgInterpFactory,
)
from argrelay.plugin_interp.FirstArgInterpFactoryConfigSchema import (
    first_arg_vals_to_next_interp_factory_ids_,
    ignored_func_ids_list_,
)
from argrelay.plugin_interp.NoopInterp import NoopInterp
from argrelay.plugin_interp.NoopInterpFactory import NoopInterpFactory
from argrelay.relay_client import __main__
from argrelay.schema_config_core_server.ServerConfigSchema import (
    server_config_desc,
    server_plugin_control_,
)
from argrelay.schema_config_core_server.ServerPluginControlSchema import composite_forest_
from argrelay.schema_config_plugin.PluginConfigSchema import plugin_instance_entries_, plugin_config_desc
from argrelay.schema_config_plugin.PluginEntrySchema import (
    plugin_config_,
    plugin_module_name_,
    plugin_class_name_,
    plugin_dependencies_,
)
from argrelay.test_infra import parse_line_and_cpos, line_no
from argrelay.test_infra.EnvMockBuilder import (
    LocalClientEnvMockBuilder,
)
from argrelay.test_infra.LocalTestClass import LocalTestClass


class ThisTestClass(LocalTestClass):
    same_test_data_per_class = "TD_63_37_05_36"  # demo

    def run_consume_test(self, test_line, expected_consumed_first_token):
        (command_line, cursor_cpos) = parse_line_and_cpos(test_line)

        first_command_names = [
            "known_command1",
            "known_command2",
        ]

        server_config_dict = server_config_desc.dict_from_default_file()
        plugin_config_dict = plugin_config_desc.dict_from_default_file()

        # Patch server config for `FirstArgInterpFactory` - bind all `first_command_names` to `NoopInterpFactory`:
        dependent_plugin_id = f"{FirstArgInterpFactory.__name__}.default"
        plugin_entry = plugin_config_dict[plugin_instance_entries_][dependent_plugin_id]
        for first_command_name in first_command_names:
            # Compose same plugin id (as below):
            plugin_instance_id = f"{NoopInterpFactory.__name__}.{first_command_name}"
            plugin_entry[plugin_config_][first_arg_vals_to_next_interp_factory_ids_][
                first_command_name
            ] = plugin_instance_id

        first_arg_vals_to_next_interp_factory_ids = plugin_entry[plugin_config_][
            first_arg_vals_to_next_interp_factory_ids_
        ]

        # List all known `func_id`-s (without using them by this plugin) to keep validation happy:
        plugin_entry[plugin_config_][ignored_func_ids_list_] = [
            "goto_service_func",
            "list_service_func",
            "diff_service_func",
            "desc_service_func",

            "goto_host_func",
            "list_host_func",
            "desc_host_func",

            "goto_git_repo_func",
            "desc_git_tag_func",
            "desc_git_commit_func",

            "funct_id_print_with_severity_level",
            "funct_id_print_with_exit_code",
            "funct_id_print_with_io_redirect",
            "funct_id_double_execution",

            "intercept_invocation_func",
            "help_hint_func",
            "query_enum_items_func",
            "echo_args_func",
        ]

        # Patch server config to add NoopInterpFactory (2 plugin instances):
        for first_command_name in first_command_names:
            # Compose same plugin id (as above):
            plugin_instance_id = f"{NoopInterpFactory.__name__}.{first_command_name}"
            plugin_entry = {
                plugin_module_name_: NoopInterpFactory.__module__,
                plugin_class_name_: NoopInterpFactory.__name__,
            }
            assert plugin_instance_id not in plugin_config_dict[plugin_instance_entries_]
            plugin_config_dict[plugin_instance_entries_][plugin_instance_id] = plugin_entry

            plugin_config_dict[
                plugin_instance_entries_
            ][dependent_plugin_id][plugin_dependencies_].append(plugin_instance_id)

            server_config_dict[server_plugin_control_][composite_forest_][tree_roots_][first_command_name] = {
                node_type_: CompositeNodeType.zero_arg_node.name,
                plugin_instance_id_: plugin_instance_id,
                sub_tree_: None,
            }

        env_mock_builder = (
            LocalClientEnvMockBuilder()
            .set_command_line(command_line)
            .set_cursor_cpos(cursor_cpos)
            .set_comp_type(CompType.PrefixShown)
            .set_server_config_dict(server_config_dict)
            .set_plugin_config_dict(plugin_config_dict)
        )
        with env_mock_builder.build():
            command_obj = __main__.main()
            assert isinstance(command_obj, AbstractLocalClientCommand)
            interp_ctx = command_obj.interp_ctx

            if not expected_consumed_first_token:
                self.assertEqual([], interp_ctx.consumed_token_ipos_list())
                return

            # FirstArgInterp is supposed to consume first pos arg only (first token):
            self.assertEqual([0], interp_ctx.consumed_token_ipos_list())
            first_token_value = interp_ctx.parsed_ctx.all_tokens[0]

            interp_factory_id = first_arg_vals_to_next_interp_factory_ids[first_token_value]
            interp_factory_instance: NoopInterpFactory = interp_ctx.interp_factories[interp_factory_id]
            prev_interp: NoopInterp = interp_ctx.prev_interp

            self.assertTrue(
                (
                    prev_interp.interp_factory_id
                    ==
                    interp_factory_instance.plugin_instance_id
                    ==
                    f"{NoopInterpFactory.__name__}.{first_token_value}"
                ),
                "config instructs to name interp instance as the first token it binds to",
            )

    def test_consume_pos_args_unknown(self):
        test_line = "unknown_command prod|"
        self.run_consume_test(test_line, None)

    def test_consume_pos_args_known(self):
        test_line = "known_command1 prod|"
        self.run_consume_test(test_line, "known_command1")
        test_line = "known_command2 prod|"
        self.run_consume_test(test_line, "known_command2")

    def test_consume_pos_args_with_no_args(self):
        test_line = "  | "
        self.run_consume_test(test_line, None)

    def test_propose_command_id(self):
        test_cases = [
            (
                line_no(), "|", CompType.PrefixHidden,
                [
                    "relay_demo",
                    "service_relay_demo",
                    "some_command",
                ],
                "This will not be called from shell - shell will suggest when command_id is already selected. "
                "Suggest registered command_id-s.",
            ),
            (
                line_no(), "r|", CompType.PrefixHidden,
                [
                    "relay_demo",
                ],
                "This will not be called from shell - shell will suggest when command_id is already selected. "
                "Suggest registered command_id-s.",
            ),
            (
                line_no(), " qwer|", CompType.PrefixHidden,
                [],
                "This will not be called from shell - shell will suggest when command_id is already selected. "
                "Suggest registered command_id-s.",
            ),
        ]

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    comp_type,
                    expected_suggestions,
                    case_comment,
                ) = test_case

                self.verify_output_with_new_server_via_local_client(
                    self.__class__.same_test_data_per_class,
                    test_line,
                    comp_type,
                    expected_suggestions,
                    None,
                    None,
                    None,
                )
