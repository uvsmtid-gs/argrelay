from argrelay.custom_integ.ServiceArgType import ServiceArgType
from argrelay.enum_desc.ArgSource import ArgSource
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.GlobalArgType import GlobalArgType
from argrelay.enum_desc.RunMode import RunMode
from argrelay.runtime_data.AssignedValue import AssignedValue
from argrelay.test_helper import line_no
from argrelay.test_helper.InOutTestCase import InOutTestCase


class ThisTestCase(InOutTestCase):

    def test_FS_88_66_66_73_intercept(self):
        """
        Test FS_88_66_66_73 `intercept` command/func
        """

        test_cases = [
            (
                line_no(),
                "some_command intercept goto service s_b prod |",
                RunMode.CompletionMode,
                CompType.PrefixShown,
                ["qwer-pd-1", "qwer-pd-2"],
                None,
                None,
                "",
            ),
            (
                line_no(),
                "some_command intercept goto service s_b prod qwer-pd-2 |",
                RunMode.InvocationMode,
                CompType.InvokeAction,
                [],
                {
                    1: {
                        GlobalArgType.ActionType.name: AssignedValue("goto", ArgSource.ExplicitPosArg),
                        GlobalArgType.ObjectSelector.name: AssignedValue("service", ArgSource.ExplicitPosArg),
                    },
                    2: {
                        ServiceArgType.ServiceName.name: AssignedValue("s_b", ArgSource.ExplicitPosArg),
                        ServiceArgType.CodeMaturity.name: AssignedValue("prod", ArgSource.ExplicitPosArg),
                        ServiceArgType.HostName.name: AssignedValue("qwer-pd-2", ArgSource.ExplicitPosArg),
                    },
                },
                None,
                "",
            ),
        ]

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    run_mode,
                    comp_type,
                    expected_suggestions,
                    envelope_ipos_to_expected_assignments,
                    invocator_class,
                    case_comment,
                ) = test_case

                self.verify_output(
                    "TD_63_37_05_36",  # demo
                    test_line,
                    run_mode,
                    comp_type,
                    expected_suggestions,
                    envelope_ipos_to_expected_assignments,
                    invocator_class,
                )
