import responses
from icecream import ic

from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.enum_desc.ServerAction import ServerAction
from argrelay.enum_desc.TermColor import TermColor
from argrelay.handler_response.DescribeLineArgsClientResponseHandler import indent_size
from argrelay.relay_client import __main__
from argrelay.schema_config_core_client.ConnectionConfigSchema import connection_config_desc
from argrelay.schema_response.ArgValuesSchema import arg_values_desc, arg_values_
from argrelay.schema_response.InterpResultSchema import interp_result_desc
from argrelay.schema_response.InvocationInputSchema import invocation_input_desc
from argrelay.server_spec.const_int import BASE_URL_FORMAT
from argrelay.test_helper import parse_line_and_cpos
from argrelay.test_helper.BaseTestCase import BaseTestCase
from argrelay.test_helper.EnvMockBuilder import LiveServerEnvMockBuilder


class ThisTestCase(BaseTestCase):
    """
    Client-only test via mocked `responses` lib (without spanning `argrelay` server).
    """

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        cls.base_URL = BASE_URL_FORMAT.format(**connection_config_desc.dict_example)

    def get_mocked_response(
        self,
        server_action: ServerAction,
        response_body: dict,
    ):
        return responses.Response(
            method = "POST",
            url = self.base_URL + server_action.value,
            json = response_body,
            status = 200,
            content_type = "application/json"
        )

    # noinspection PyMethodMayBeStatic
    def get_env_mock_builder(
        self,
        comp_type: CompType,
    ):
        # Because response is mocked, it has nothing to do with this client request:
        test_line = "some_command pro|d whatever"
        (command_line, cursor_cpos) = parse_line_and_cpos(test_line)

        env_mock_builder = (
            # Using "LiveServer*" because we do not manage server in the test,
            # but we mock it outside `EnvMockBuilder`:
            LiveServerEnvMockBuilder()
            .set_mock_client_config_file_read(True)
            .set_client_config_dict()
            .set_client_config_to_optimize_completion_request(False)
            .set_command_line(command_line)
            .set_cursor_cpos(cursor_cpos)
            .set_comp_type(comp_type)
            .set_capture_stdout(True)
            .set_capture_stderr(True)
        )
        return env_mock_builder

    @responses.activate
    def test_mocked_DescribeLineArgs_response(self):
        responses.add(self.get_mocked_response(
            ServerAction.DescribeLineArgs,
            interp_result_desc.dict_example,
        ))
        env_mock_builder = self.get_env_mock_builder(CompType.DescribeArgs)
        with env_mock_builder.build():
            __main__.main()
            self.assertEqual(
                "",
                env_mock_builder.actual_stderr.getvalue(),
            )
            self.assertEqual(
                f"""
{TermColor.consumed_token.value}some_command{TermColor.reset_style.value} {TermColor.prefix_highlight.value}{TermColor.tangent_token_l_part.value}unrecognized_{TermColor.reset_style.value}{TermColor.tangent_token_r_part.value}token{TermColor.reset_style.value} {TermColor.consumed_token.value}goto{TermColor.reset_style.value} {TermColor.consumed_token.value}host{TermColor.reset_style.value} {TermColor.consumed_token.value}prod{TermColor.reset_style.value} 
{ReservedEnvelopeClass.ClassFunction.name}: 1
{" " * indent_size}{TermColor.no_option_to_suggest.value}TypeA: [none]{TermColor.reset_style.value}
{" " * indent_size}{TermColor.no_option_to_suggest.value}TypeB: [none]{TermColor.reset_style.value}
""",

                ic(env_mock_builder.actual_stdout.getvalue()),
            )

    @responses.activate
    def test_mocked_ProposeArgValues_response(self):
        responses.add(self.get_mocked_response(
            ServerAction.ProposeArgValues,
            arg_values_desc.dict_example,
        ))
        env_mock_builder = self.get_env_mock_builder(CompType.PrefixShown)
        with env_mock_builder.build():
            __main__.main()
            self.assertEqual(
                "",
                env_mock_builder.actual_stderr.getvalue(),
            )
            self.assertEqual(
                "\n".join(arg_values_desc.dict_example[arg_values_]) + "\n",
                ic(env_mock_builder.actual_stdout.getvalue()),
            )

    @responses.activate
    def test_mocked_RelayLineArgs_response(self):
        responses.add(self.get_mocked_response(
            ServerAction.RelayLineArgs,
            invocation_input_desc.dict_example,
        ))
        env_mock_builder = self.get_env_mock_builder(CompType.InvokeAction)
        with env_mock_builder.build():
            __main__.main()
            self.assertEqual(
                "",
                env_mock_builder.actual_stderr.getvalue(),
            )
            self.assertEqual(
                "",
                ic(env_mock_builder.actual_stdout.getvalue()),
            )
