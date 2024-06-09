from argrelay.custom_integ.ServicePropName import ServicePropName
from argrelay.custom_integ.ServiceEnvelopeClass import ServiceEnvelopeClass
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.ReservedPropName import ReservedPropName
from argrelay.plugin_delegator.ErrorDelegator import ErrorDelegator
from argrelay.relay_client import __main__
from argrelay.test_infra import parse_line_and_cpos
from argrelay.test_infra.EnvMockBuilder import (
    EnvMockBuilder,
    LiveServerEnvMockBuilder,
)
from env_tests.ManualServerTestClass import ManualServerTestClass


# TODO: Do we really need this test? Why not using `RemoteTestClass` or `End2EndTestClass`?
class ThisTestClass(ManualServerTestClass):

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
                invocation_input.envelope_containers[1].data_envelopes[0][ReservedPropName.envelope_class.name]
            )
            self.assertEqual(
                "prod-apac-downstream",
                invocation_input.envelope_containers[1].data_envelopes[0][ServicePropName.cluster_name.name]
            )
            self.assertEqual(
                "wert-pd-1",
                invocation_input.envelope_containers[1].data_envelopes[0][ServicePropName.host_name.name]
            )
            self.assertEqual(
                "tt1",
                invocation_input.envelope_containers[1].data_envelopes[0][ServicePropName.service_name.name]
            )
            self.assertTrue(True)
