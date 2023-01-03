from __future__ import annotations

from unittest import TestCase

from argrelay.meta_data.ArgSource import ArgSource
from argrelay.meta_data.ArgValue import ArgValue
from argrelay.meta_data.CompType import CompType
from argrelay.meta_data.RunMode import RunMode
from argrelay.meta_data.TermColor import TermColor
from argrelay.relay_client.__main__ import main
from argrelay.relay_demo.ServiceArgType import ServiceArgType
from argrelay.runtime_context.InterpContext import assigned_types_to_values_
from misc_helper import line_no, parse_line_and_cpos
from misc_helper.EnvMockBuilder import (
    EnvMockBuilder
)


class ThisTestCase(TestCase):

    def test_propose_auto_comp(self):
        # @formatter:off
        test_cases = [
            (line_no(), "some_command |", CompType.PrefixHidden, "goto\ndesc\nlist", "Suggest from the set of values for the first unassigned arg type"),
            (line_no(), "some_command goto host prod amer upstream sdfg|  ", CompType.PrefixShown, "sdfg", "Still as expected with trailing space after cursor"),
            (line_no(), "some_command goto host qa prod|", CompType.SubsequentHelp, "", "Another value from the same dimension with `SubsequentHelp` => no suggestions"),
            (line_no(), "some_command host qa upstream amer qw goto ro service_c green |", CompType.PrefixShown, "", "No more suggestions when all coordinates specified"),
            (line_no(), "some_command host qa goto |", CompType.MenuCompletion, "upstream\ndownstream", "Suggestions for next coordinate show entire space"),
            (line_no(), "some_command upstream goto host |", CompType.PrefixHidden, "dev\nqa\nprod", ""),
            (line_no(), "some_command upstream goto host |",  CompType.SubsequentHelp, "dev\nqa\nprod", ""),
            # TODO: If selected token left part does not fall into next expected space, suggest from all other (yet not determined) matching that substring.
            (line_no(), "some_command host goto upstream q|", CompType.SubsequentHelp, "qa\nqw\nqwe\nqwer", "Suggestions for subsequent Tab are limited by prefix"),
            (line_no(), "some_command upstream qa apac desc |", CompType.SubsequentHelp, "qw\nqwe\nqwer\nwert\nas\nasd\nasdf\nsdfg\nzx\nzxc\nzxcv\nxcvb", ""),
            (line_no(), "some_command service upstream|", CompType.PrefixHidden, "upstream", ""),
            (line_no(), "some_command de|", CompType.PrefixHidden, "desc", "Suggest from the set of values for the first unassigned arg type (with matching prefix)"),
            (line_no(), "some_command host goto q| dev", CompType.PrefixHidden, "qw\nqwe\nqwer", "Suggestion for a value from other spaces which do not have coordinate specified"),
            (line_no(), "some_command q| dev", CompType.PrefixHidden, "", "Do not suggest a value from other spaces until they are available for query for current object to search"),
            (line_no(), "some_command pro| dev", CompType.PrefixHidden, "", "No suggestion for another value from a space which already have coordinate specified"),
            (line_no(), "some_command goto service q| whatever", CompType.PrefixHidden, "qa", "Unrecognized value does not obstruct suggestion"),
        ]
        # @formatter:on

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    comp_type,
                    expected_suggestions,
                    case_comment,
                ) = test_case
                (command_line, cursor_cpos) = parse_line_and_cpos(test_line)

                env_mock_builder = (
                    EnvMockBuilder()
                    .set_run_mode(RunMode.CompletionMode)
                    .set_command_line(command_line)
                    .set_cursor_cpos(cursor_cpos)
                    .set_comp_type(comp_type)
                )
                with env_mock_builder.build():
                    interp_ctx = main()

                    actual_suggestions = interp_ctx.propose_auto_comp()
                    self.assertEqual(expected_suggestions, actual_suggestions)

    def test_describe_args(self):
        # @formatter:off
        test_cases = [
            (line_no(), "some_command goto service prod amer upstream sdfg|  ", CompType.DescribeArgs, "sdfg", ""),
        ]
        # @formatter:on

        for test_case in test_cases:
            with self.subTest(test_case):
                (
                    line_number,
                    test_line,
                    comp_type,
                    expected_suggestions,
                    case_comment
                ) = test_case
                (command_line, cursor_cpos) = parse_line_and_cpos(test_line)

                env_mock_builder = (
                    EnvMockBuilder()
                    .set_run_mode(RunMode.CompletionMode)
                    .set_command_line(command_line)
                    .set_cursor_cpos(cursor_cpos)
                    .set_comp_type(comp_type)
                )
                with env_mock_builder.build():
                    interp_ctx = main()

                    # Nested to capture output only after all processing output is over (ready for action output):
                    with (
                        EnvMockBuilder()
                            .set_mock_mongo_client(False)
                            .set_capture_stderr(True)
                            .build()
                    ):
                        interp_ctx.invoke_action()

                        self.maxDiff = None
                        # TODO: Fix: currently (after extending data schema)
                        #       what this output shows is entire type list known to static data (it should use limited lists per object)
                        #       and it only compares it to the last `curr_assigned_types_to_values` (while it should print all `assigned_types_to_values_per_object`)
                        self.assertEqual(
                            f"""
{TermColor.BRIGHT_YELLOW.value}*AccessType: ?{TermColor.RESET.value} ro|rw
{TermColor.BRIGHT_YELLOW.value}ActionType: ?{TermColor.RESET.value} goto|desc|list
{TermColor.DARK_GREEN.value}CodeMaturity: prod [ExplicitArg]{TermColor.RESET.value}
{TermColor.BRIGHT_YELLOW.value}ColorTag: ?{TermColor.RESET.value} red|green
{TermColor.DARK_GREEN.value}FlowStage: upstream [ExplicitArg]{TermColor.RESET.value}
{TermColor.DARK_GREEN.value}GeoRegion: amer [ExplicitArg]{TermColor.RESET.value}
{TermColor.BRIGHT_YELLOW.value}HostName: ?{TermColor.RESET.value} qw|qwe|qwer|wert|as|asd|asdf|sdfg|zx|zxc|zxcv|xcvb
{TermColor.BRIGHT_YELLOW.value}ObjectSelector: ?{TermColor.RESET.value} host|service
{TermColor.BRIGHT_YELLOW.value}ServiceName: ?{TermColor.RESET.value} service_a|service_b|service_c
""",
                            env_mock_builder.actual_stderr.getvalue()
                        )

    def test_arg_assignments_for_completion(self):
        # @formatter:off
        test_cases = [
            # TODO: uncomment, it works:
            (line_no(), RunMode.CompletionMode, "some_command goto|", CompType.PrefixShown, 0, {ServiceArgType.ActionType.name: None, ServiceArgType.ObjectSelector.name: None}, "No assignment for incomplete token (token pointed by the cursor) in completion mode"),
            (line_no(), RunMode.InvocationMode, "some_command goto|", CompType.PrefixShown, 0, {ServiceArgType.ActionType.name: ArgValue("goto", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: None}, "Incomplete token (pointed by the cursor) is complete in invocation mode"),

            (line_no(), RunMode.CompletionMode, "some_command goto |", CompType.PrefixShown, 0, {ServiceArgType.ActionType.name: ArgValue("goto", ArgSource.ExplicitArg), ServiceArgType.ObjectSelector.name: None}, "Explicit assignment for complete token"),
            (line_no(), RunMode.CompletionMode, "some_command goto service |", CompType.PrefixShown, 0, {ServiceArgType.ActionType.name: ArgValue("goto", ArgSource.ExplicitArg), ServiceArgType.ObjectSelector.name: ArgValue("service", ArgSource.ExplicitArg)}, "Explicit assignment for complete token"),

            (line_no(), RunMode.CompletionMode, "some_command goto host prod|", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: None, ServiceArgType.AccessType.name: None}, "No implicit assignment for incomplete token"),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            #(line_no(), RunMode.InvocationMode, "some_command goto host prod|", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: ArgValue("prod", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: ArgValue("ro", ArgSource.ImplicitValue)}, "Implicit assignment even for incomplete token (token pointed by cursor)"),

            (line_no(), RunMode.CompletionMode, "some_command goto host prod |", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: ArgValue("prod", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: None}, "No implicit assignment of access type to \"ro\" when code maturity is \"prod\" in completion"),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            #(line_no(), RunMode.InvocationMode, "some_command goto host prod |", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: ArgValue("prod", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: ArgValue("ro", ArgSource.ImplicitValue)}, "Implicit assignment of access type to \"ro\" when code maturity is \"prod\" in invocation"),

            (line_no(), RunMode.CompletionMode, "some_command goto host dev |", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: ArgValue("dev", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: None}, "No implicit assignment of access type to \"rw\" when code maturity is \"dev\" in completion"),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            #(line_no(), RunMode.InvocationMode, "some_command goto host dev |", CompType.PrefixShown, 1, {ServiceArgType.CodeMaturity.name: ArgValue("dev", ArgSource.ExplicitArg), ServiceArgType.AccessType.name: ArgValue("rw", ArgSource.ImplicitValue)}, "Implicit assignment of access type to \"rw\" when code maturity is \"uat\" in invocation"),
        ]
        # @formatter:on

        for test_case in test_cases:

            with self.subTest(test_case):
                (
                    line_number,
                    run_mode,
                    test_line,
                    comp_type,
                    found_object_ipos,
                    expected_assignments,
                    case_comment,
                ) = test_case
                (command_line, cursor_cpos) = parse_line_and_cpos(test_line)
                env_mock_builder = (
                    EnvMockBuilder()
                    .set_run_mode(run_mode)
                    .set_command_line(command_line)
                    .set_cursor_cpos(cursor_cpos)
                    .set_comp_type(comp_type)
                )
                with env_mock_builder.build():

                    interp_ctx = main()

                    for arg_type, arg_value in expected_assignments.items():
                        if arg_value is None:
                            self.assertTrue(
                                arg_type not in
                                interp_ctx.assigned_types_to_values_per_object
                                [found_object_ipos]
                                [assigned_types_to_values_]
                            )
                        else:
                            self.assertEqual(
                                arg_value,
                                interp_ctx.assigned_types_to_values_per_object
                                [found_object_ipos]
                                [assigned_types_to_values_]
                                [arg_type]
                            )