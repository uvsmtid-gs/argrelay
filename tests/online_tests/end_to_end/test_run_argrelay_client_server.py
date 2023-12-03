from argrelay.enum_desc.ArgSource import ArgSource
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.enum_desc.TermColor import TermColor
from argrelay.handler_response.DescribeLineArgsClientResponseHandler import indent_size
from argrelay.plugin_interp.FuncTreeInterpFactory import func_envelope_path_step_prop_name
from argrelay.test_infra import change_to_known_repo_path, line_no
from argrelay.test_infra.End2EndTestClass import (
    End2EndTestClass,
)


# noinspection PyMethodMayBeStatic
class ThisTestClass(End2EndTestClass):

    def test_DescribeLineArgs(self):
        """
        Invokes client via generated `@/bin/run_argrelay_client` sending `ServerAction.DescribeArgs`.
        """

        # @formatter:off
        test_cases = [
            (
                line_no(), f"{self.default_bound_command} goto h|",
                f"""
{TermColor.consumed_token.value}{self.default_bound_command}{TermColor.reset_style.value} {TermColor.consumed_token.value}goto{TermColor.reset_style.value} {TermColor.prefix_highlight.value}{TermColor.tangent_token_l_part.value}h{TermColor.reset_style.value}{TermColor.tangent_token_r_part.value}{TermColor.reset_style.value} 
{ReservedEnvelopeClass.ClassFunction.name}: {TermColor.found_count_n.value}3{TermColor.reset_style.value}
{" " * indent_size}{TermColor.other_assigned_arg_value.value}{func_envelope_path_step_prop_name(0)}: relay_demo {TermColor.other_assigned_arg_value.value}[{ArgSource.InitValue.name}]{TermColor.reset_style.value}
{" " * indent_size}{TermColor.explicit_pos_arg_value.value}{func_envelope_path_step_prop_name(1)}: goto {TermColor.explicit_pos_arg_value.value}[{ArgSource.ExplicitPosArg.name}]{TermColor.reset_style.value}
{" " * indent_size}{TermColor.remaining_value.value}*{func_envelope_path_step_prop_name(2)}: ?{TermColor.reset_style.value} repo {TermColor.prefix_highlight.value}{TermColor.tangent_token_l_part.value}h{TermColor.reset_style.value}{TermColor.tangent_token_r_part.value}ost{TermColor.reset_style.value} service 
""",
                "Test sample 1",
            ),
            (
                line_no(), f"{self.default_bound_command} goto s|",
                f"""
{TermColor.consumed_token.value}{self.default_bound_command}{TermColor.reset_style.value} {TermColor.consumed_token.value}goto{TermColor.reset_style.value} {TermColor.prefix_highlight.value}{TermColor.tangent_token_l_part.value}s{TermColor.reset_style.value}{TermColor.tangent_token_r_part.value}{TermColor.reset_style.value} 
{ReservedEnvelopeClass.ClassFunction.name}: {TermColor.found_count_n.value}3{TermColor.reset_style.value}
{" " * indent_size}{TermColor.other_assigned_arg_value.value}{func_envelope_path_step_prop_name(0)}: relay_demo {TermColor.other_assigned_arg_value.value}[{ArgSource.InitValue.name}]{TermColor.reset_style.value}
{" " * indent_size}{TermColor.explicit_pos_arg_value.value}{func_envelope_path_step_prop_name(1)}: goto {TermColor.explicit_pos_arg_value.value}[{ArgSource.ExplicitPosArg.name}]{TermColor.reset_style.value}
{" " * indent_size}{TermColor.remaining_value.value}*{func_envelope_path_step_prop_name(2)}: ?{TermColor.reset_style.value} repo host {TermColor.prefix_highlight.value}{TermColor.tangent_token_l_part.value}s{TermColor.reset_style.value}{TermColor.tangent_token_r_part.value}ervice{TermColor.reset_style.value} 
""",
                "Test sample 2",
            ),
        ]
        # @formatter:on

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    expected_stdout_str,
                    case_comment,
                ) = test_case
                with change_to_known_repo_path("."):
                    self.assert_DescribeLineArgs(
                        self.default_bound_command,
                        test_line,
                        expected_stdout_str,
                    )

    def test_DescribeLineArgs_fails(self):
        with self.assertRaises(AssertionError):
            with change_to_known_repo_path("."):
                self.assert_ProposeArgValues(
                    self.default_bound_command,
                    f"{self.default_bound_command} goto h|",
                    CompType.PrefixShown,
                    "whatever",
                    1,
                )

    def test_ProposeArgValues(self):
        """
        Invokes client via generated `@/bin/run_argrelay_client` sending `ServerAction.ProposeArgValues`.
        """

        # @formatter:off
        test_cases = [
            (
                line_no(), f"{self.default_bound_command} desc host dev upstream |",
                CompType.PrefixShown,
                f"""apac
emea
amer
""",
                "Test sample 1",
            ),
            (
                line_no(), f"{self.default_bound_command} desc host dev upstream a|",
                CompType.SubsequentHelp,
                f"""apac
amer
""",
                "Test sample 2",
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
                    case_comment,
                ) = test_case
                with change_to_known_repo_path("."):
                    self.assert_ProposeArgValues(
                        self.default_bound_command,
                        test_line,
                        comp_type,
                        expected_stdout_str,
                    )

    def test_ProposeArgValues_fails(self):
        with self.assertRaises(AssertionError):
            with change_to_known_repo_path("."):
                self.assert_ProposeArgValues(
                    self.default_bound_command,
                    f"{self.default_bound_command} desc host dev upstream |",
                    CompType.PrefixShown,
                    "whatever",
                    1,
                )

    def test_RelayLineArgs(self):
        """
        Invokes client via generated `@/bin/run_argrelay_client` sending `ServerAction.RelayLineArgs`.
        """

        # @formatter:off
        test_cases = [
            (
                line_no(), f"{self.default_bound_command} desc host dev upstream amer".split(" "),
                0,
                "",
                "",
                "`NoopDelegator` executes successfully without any output.",
            ),
            (
                line_no(), f"{self.default_bound_command} echo one two three four five".split(" "),
                0,
                f"{self.default_bound_command} echo one two three four five\n",
                "",
                "FS_43_50_57_71: `echo_args` func executes successfully printing its args.",
            ),
            (
                line_no(), f"{self.default_bound_command} goto host dev upstream amer".split(" "),
                0,
                "",
                "INFO: command executed successfully: demo implementation is a stub" + "\n",
                "`ErrorDelegator` executes successfully with output on STDERR.",
            ),
        ]
        # @formatter:on

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    command_line_args,
                    expected_exit_code,
                    expected_stdout_str,
                    expected_stderr_str,
                    case_comment,
                ) = test_case
                with change_to_known_repo_path("."):
                    self.assert_RelayLineArgs(
                        command_line_args,
                        expected_exit_code,
                        expected_stdout_str,
                        expected_stderr_str,
                    )
