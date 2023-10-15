from argrelay.custom_integ.ServiceArgType import ServiceArgType
from argrelay.custom_integ.ServiceEnvelopeClass import ServiceEnvelopeClass
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.ReservedArgType import ReservedArgType
from argrelay.plugin_delegator.ErrorDelegator import ErrorDelegator
from argrelay.relay_client import __main__
from argrelay.test_helper import parse_line_and_cpos
from argrelay.test_helper.EnvMockBuilder import (
    EnvMockBuilder,
    LiveServerEnvMockBuilder,
)
from env_tests.ManualServerTest import ManualServerTest


# TODO: Do we really need this test? Why not using `RemoteTestCase` or `End2EndTestCase`?
class ThisTestCase(ManualServerTest):

    # noinspection PyMethodMayBeStatic
    def test_live_relay_line_args(self):
        test_line = "some_command goto service prod downstream wert-pd-1 |"
        (command_line, cursor_cpos) = parse_line_and_cpos(test_line)
        env_mock_builder = (
            LiveServerEnvMockBuilder()
            .set_command_line(command_line)
            .set_cursor_cpos(cursor_cpos)
            .set_comp_type(CompType.InvokeAction)
            .set_capture_delegator_invocation_input(ErrorDelegator)
        )
        with env_mock_builder.build():
            __main__.main()
            print(EnvMockBuilder.invocation_input)
            invocation_input = EnvMockBuilder.invocation_input
            self.assertEqual(
                ServiceEnvelopeClass.ClassService.name,
                invocation_input.envelope_containers[1].data_envelopes[0][ReservedArgType.EnvelopeClass.name]
            )
            self.assertEqual(
                "prod-apac-downstream",
                invocation_input.envelope_containers[1].data_envelopes[0][ServiceArgType.ClusterName.name]
            )
            self.assertEqual(
                "wert-pd-1",
                invocation_input.envelope_containers[1].data_envelopes[0][ServiceArgType.HostName.name]
            )
            self.assertEqual(
                "tt1",
                invocation_input.envelope_containers[1].data_envelopes[0][ServiceArgType.ServiceName.name]
            )
            self.assertTrue(True)
