from argrelay.enum_desc.CompType import CompType
from argrelay.test_helper import change_to_known_repo_path, line_no
from argrelay.test_helper.End2EndTestCase import (
    End2EndTestCase,
)


class ThisTestCase(End2EndTestCase):

    def test_ProposeArgValuesRemoteOptimizedClientCommand_sends_valid_JSON_for_commands_with_quotes(self):
        """
        Invokes client via generated `@/bin/run_argrelay_client` sending `ServerAction.ProposeArgValues`.
        """

        # @formatter:off
        test_cases = [
            (
                line_no(), f"{self.default_bound_command} desc host dev \"some_unrecognized_token upstream |",
                CompType.PrefixShown,
                f"""apac
emea
amer
""",
            ),
            (
                line_no(), f"{self.default_bound_command} desc host dev \"some_unrecognized_token\" upstream a|",
                CompType.SubsequentHelp,
                f"""apac
amer
""",
            ),
        ]
        # @formatter:on

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    comp_type,
                    expected_stdout_str,
                ) = test_case
                with change_to_known_repo_path("."):
                    self.assert_ProposeArgValues(
                        self.default_bound_command,
                        test_line,
                        comp_type,
                        expected_stdout_str,
                    )
