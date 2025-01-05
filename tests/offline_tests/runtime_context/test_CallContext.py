import os

import argrelay
from argrelay.client_spec.ShellContext import UNKNOWN_COMP_KEY, ShellContext, get_user_name, get_client_conf_target
from argrelay.enum_desc.CompScope import CompScope
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.ServerAction import ServerAction
from argrelay.test_infra import line_no, parse_line_and_cpos
from argrelay.test_infra.BaseTestClass import BaseTestClass
from argrelay_api_server_cli.schema_request.CallContextSchema import (
    call_context_desc,
    client_pid_,
    is_debug_enabled_,
    server_action_,
    comp_scope_,
    cursor_cpos_,
    command_line_,
    client_uid_,
    client_conf_target_,
    client_version_,
    input_data_,
)


class ThisTestClass(BaseTestClass):

    def test_to_json(self):
        """
        Test CallContext JSON-dump
        """

        test_cases = [
            (
                line_no(), "basic conversion",
                "some_command prod amer upstream sdfg|  ", CompType.PrefixShown,
                f'{{'
                f'"{client_version_}": "{argrelay.__version__}", '
                f'"{client_conf_target_}": "{get_client_conf_target()}", '
                f'"{server_action_}": "{ServerAction.ProposeArgValues.name}", '
                f'"{command_line_}": "some_command prod amer upstream sdfg  ", '
                f'"{cursor_cpos_}": 36, '
                f'"{comp_scope_}": "{CompScope.ScopeInitial.name}", '
                f'"{client_uid_}": "{get_user_name()}", '
                f'"{client_pid_}": {os.getpid()}, '
                f'"{is_debug_enabled_}": false, '
                f'"{input_data_}": null'
                f'}}',
            ),
        ]
        for test_case in test_cases:
            with self.subTest(test_case):
                (line_number, case_comment, test_line, comp_type, expected_json) = test_case
                (command_line, cursor_cpos) = parse_line_and_cpos(test_line)
                call_ctx = ShellContext(
                    command_line = command_line,
                    cursor_cpos = cursor_cpos,
                    comp_type = comp_type,
                    is_debug_enabled = False,
                    comp_key = UNKNOWN_COMP_KEY,
                    input_data = None,
                ).create_call_context()
                actual_json = call_context_desc.dict_schema.dumps(call_ctx)
                self.assertEqual(expected_json, actual_json)
