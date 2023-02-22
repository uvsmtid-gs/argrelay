from __future__ import annotations

from unittest import TestCase, skip

from argrelay.client_command_local.AbstractLocalClientCommand import AbstractLocalClientCommand
from argrelay.custom_integ.ServiceArgType import ServiceArgType
from argrelay.custom_integ.ServiceEnvelopeClass import ServiceEnvelopeClass
from argrelay.enum_desc.ArgSource import ArgSource
from argrelay.enum_desc.CompType import CompType
from argrelay.enum_desc.GlobalArgType import GlobalArgType
from argrelay.enum_desc.ReservedArgType import ReservedArgType
from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.enum_desc.RunMode import RunMode
from argrelay.enum_desc.TermColor import TermColor
from argrelay.plugin_invocator.ErrorInvocator import ErrorInvocator
from argrelay.relay_client import __main__
from argrelay.runtime_context.EnvelopeContainer import EnvelopeContainer, indent_size
from argrelay.runtime_data.AssignedValue import AssignedValue
from argrelay.schema_response.ArgValuesSchema import arg_values_
from argrelay.test_helper import line_no, parse_line_and_cpos
from argrelay.test_helper.EnvMockBuilder import (
    EnvMockBuilder
)


class ThisTestCase(TestCase):

    def run_completion_mode_test(
        self,
        test_data_filter,
        command_line,
        comp_type,
        cursor_cpos,
        expected_suggestions,
    ):
        env_mock_builder = (
            EnvMockBuilder()
            .set_run_mode(RunMode.CompletionMode)
            .set_command_line(command_line)
            .set_cursor_cpos(cursor_cpos)
            .set_comp_type(comp_type)
            .set_test_data_ids_to_load(test_data_filter)
        )
        with env_mock_builder.build():
            command_obj = __main__.main()
            assert isinstance(command_obj, AbstractLocalClientCommand)

            actual_suggestions = "\n".join(command_obj.response_dict[arg_values_])
            self.assertEqual(expected_suggestions, actual_suggestions)

    def test_propose_auto_comp_TD_63_37_05_36_default(self):
        """
        Test arg values suggestion with TD_63_37_05_36 # demo
        """
        # @formatter:off
        test_cases = [
            # TODO: If tangent token left part does not fall into next expected space, in case of `CompType.SubsequentHelp` suggest to specify named arg.

            # TODO: Test that even multiple envelopes can set `ArgSource.ImplicitValue` when one of the arg type has single value among all those envelopes. Add special test data.

            (
                line_no(), "some_command |", CompType.PrefixHidden,
                "goto\ndesc\nlist",
                "Suggest from the set of values for the first unassigned arg type",
            ),
            (
                line_no(), "some_command goto host dev amer upstream qwer|  ", CompType.PrefixShown,
                "",
                "FS_23_62_89_43: "
                "Host `qwer` is already singled out `data_envelope` "
                "(only one `ServiceEnvelopeClass.ClassHost` within current `ServiceArgType.ClusterName`),"
                "therefore, it is not suggested.",
            ),
            (
                line_no(), "some_command goto host qa prod|", CompType.SubsequentHelp,
                "",
                "Another value from the same dimension with `SubsequentHelp` "
                "yet prefix not matching any from other dimensions => no suggestions",
            ),
            (
                line_no(), "some_command goto host prod apac|", CompType.SubsequentHelp,
                "",
                "FS_23_62_89_43: "
                "`ServiceArgType.CodeMaturity` = `prod` singles out `ServiceEnvelopeClass.ClassCluster` which "
                "skips suggestion for `ServiceArgType.GeoRegion`",
            ),
            (
                line_no(), "some_command host qa upstream amer qw goto ro s_c green |", CompType.PrefixShown,
                "",
                "No more suggestions when all \"coordinates\" specified",
            ),
            (
                line_no(), "some_command upstream goto host |", CompType.PrefixHidden,
                "dev\nqa",
                "`PrefixHidden`: arg values for `ClusterName` search is specified ahead function query "
                "but order is \"ignored\"",
            ),
            (
                line_no(), "some_command upstream goto host |", CompType.SubsequentHelp,
                "dev\nqa",
                "`SubsequentHelp` behaves the same way as `PrefixHidden`",
            ),
            (
                line_no(), "some_command host goto upstream a|", CompType.SubsequentHelp,
                "amer\napac",
                "Suggestions for subsequent Tab are limited by prefix",
            ),
            (
                line_no(),
                "some_command goto upstream qa apac desc host |", CompType.SubsequentHelp,
                "ro\nrw",
                "FS_23_62_89_43: "
                "`ServiceArgType.CodeMaturity` = `qa` singles out `ServiceEnvelopeClass.ClassCluster` which "
                "skips suggestion for `ServiceArgType.GeoRegion`, then this cluster has only one "
                "`ServiceEnvelopeClass.ClassHost` = `sdfg` which also skips host suggestion "
                "leaving `ServiceArgType.AccessType` to be the next to suggest.",
            ),
            (
                line_no(), "some_command service goto upstream|", CompType.PrefixHidden,
                "upstream",
                "",
            ),
            (
                line_no(), "some_command de|", CompType.PrefixHidden,
                "desc",
                "Suggest from the set of values for the first unassigned arg type (with matching prefix)",
            ),
            (
                line_no(), "some_command host goto e| dev", CompType.PrefixHidden,
                "emea",
                "Suggestion for a value from other spaces which do not have \"coordinate\" specified",
            ),
            (
                line_no(), "some_command q| dev", CompType.PrefixHidden,
                "",
                "Do not suggest a value from other spaces until "
                "they are available for query for current envelope to search",
            ),
            (
                line_no(), "some_command pro| dev", CompType.PrefixHidden,
                "",
                "No suggestion for another value from a space which already have \"coordinate\" specified",
            ),
            (
                line_no(), "some_command goto service q| whatever", CompType.PrefixHidden,
                "qa",
                "Unrecognized value does not obstruct suggestion",
            ),
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

                self.run_completion_mode_test(
                    ["TD_63_37_05_36"],  # demo
                    command_line,
                    comp_type,
                    cursor_cpos,
                    expected_suggestions,
                )

    # TODO: Fix test_data: TD_76_09_29_31: # overlapped:
    #       there is no overlap after introduction of ClusterName.
    @skip
    def test_propose_auto_comp_TD_76_09_29_31_overlapped(self):
        """
        Test arg values suggestion with TD_76_09_29_31 # overlapped
        """

        # @formatter:off
        test_cases = [
              (
                line_no(), "some_command host dev goto downstream |", CompType.MenuCompletion,
                "emea\namer.us",
                "Suggestions for next \"coordinate\" are arg values pre-filtered by selection of previous arg values",
            ),
            # TODO: Fix test_data: TD_76_09_29_31: # overlapped:
            #       there is no overlap after introduction of ClusterName.
            (
                line_no(), "some_command goto host dev downstream amer.us amer.u|", CompType.PrefixShown,
                "",
                "TD_76_09_29_31 # overlapped: one of the explicit value matches more than one type, "
                "but it is not assigned to all arg types => some suggestion for missing arg types",
            ),
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

                self.run_completion_mode_test(
                    ["TD_76_09_29_31"],  # overlapped
                    command_line,
                    comp_type,
                    cursor_cpos,
                    expected_suggestions,
                )

    def test_describe_args(self):
        # @formatter:off
        test_cases = [
            (
                line_no(), "some_command goto service dev amer upstream sdfg|  ", CompType.DescribeArgs,
                "",
                f"""
{ReservedEnvelopeClass.ClassFunction.name}:
{" " * indent_size}{TermColor.DARK_GREEN.value}ActionType: goto [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}ObjectSelector: service [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{ServiceEnvelopeClass.ClassCluster.name}:
{" " * indent_size}{TermColor.DARK_GREEN.value}CodeMaturity: dev [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}FlowStage: upstream [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}GeoRegion: amer [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{ServiceEnvelopeClass.ClassService.name}:
{" " * indent_size}{TermColor.DARK_GREEN.value}ClusterName: dev-amer-upstream [{ArgSource.InitValue.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}HostName: qwer-du [{ArgSource.ImplicitValue.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}ServiceName: s_a [{ArgSource.ImplicitValue.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GRAY.value}LiveStatus: [none]{TermColor.RESET.value}
{ServiceArgType.AccessType.name}:
{" " * indent_size}{TermColor.BRIGHT_YELLOW.value}*AccessType: ?{TermColor.RESET.value} ro|rw
""",
            ),
            (
                line_no(), "some_command goto host upstream emea|", CompType.DescribeArgs,
                "",
                f"""
{ReservedEnvelopeClass.ClassFunction.name}:
{" " * indent_size}{TermColor.DARK_GREEN.value}ActionType: goto [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GREEN.value}ObjectSelector: host [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{ServiceEnvelopeClass.ClassCluster.name}:
{" " * indent_size}{TermColor.BRIGHT_YELLOW.value}*CodeMaturity: ?{TermColor.RESET.value} dev|qa
{" " * indent_size}{TermColor.DARK_GREEN.value}FlowStage: upstream [{ArgSource.ExplicitPosArg.name}]{TermColor.RESET.value}
{" " * indent_size}{TermColor.BRIGHT_YELLOW.value}GeoRegion: ?{TermColor.RESET.value} amer|emea|apac
{ServiceEnvelopeClass.ClassHost.name}:
{" " * indent_size}{TermColor.DARK_GRAY.value}ClusterName: [none]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GRAY.value}HostName: [none]{TermColor.RESET.value}
{" " * indent_size}{TermColor.DARK_GRAY.value}LiveStatus: [none]{TermColor.RESET.value}
{ServiceArgType.AccessType.name}:
{" " * indent_size}{TermColor.DARK_GRAY.value}AccessType: [none]{TermColor.RESET.value}
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
                    case_comment,
                    stderr_output,
                ) = test_case
                (command_line, cursor_cpos) = parse_line_and_cpos(test_line)

                outer_env_mock_builder = (
                    EnvMockBuilder()
                    .set_run_mode(RunMode.CompletionMode)
                    .set_command_line(command_line)
                    .set_cursor_cpos(cursor_cpos)
                    .set_comp_type(comp_type)
                    .set_test_data_ids_to_load([
                        "TD_63_37_05_36",  # demo
                    ])
                )
                with outer_env_mock_builder.build():
                    command_obj = __main__.main()
                    assert isinstance(command_obj, AbstractLocalClientCommand)
                    interp_ctx = command_obj.interp_ctx

                    # TODO: Running print again with capturing `stderr`
                    #       (executing end-to-end above generates noise output by server logic).
                    #       A proper implementation would be getting `DescribeArgs`'s response_dict
                    #       and printing it again.
                    inner_env_mock_builder = (
                        EnvMockBuilder()
                        .set_mock_mongo_client(False)
                        .set_capture_stderr(True)
                    )
                    with inner_env_mock_builder.build():
                        EnvelopeContainer.print_help(interp_ctx.envelope_containers)

                        self.maxDiff = None
                        self.assertEqual(
                            stderr_output,
                            inner_env_mock_builder.actual_stderr.getvalue()
                        )

    def test_arg_assignments_for_completion(self):
        # @formatter:off
        test_cases = [
            (
                line_no(), RunMode.CompletionMode, "some_command goto|", CompType.PrefixShown,
                0,
                {
                    GlobalArgType.ActionType.name: None,
                    GlobalArgType.ObjectSelector.name: None,
                },
                "No assignment for incomplete token (token pointed by the cursor) in completion mode",
            ),
            (
                line_no(), RunMode.InvocationMode, "some_command desc host zxcv|", CompType.PrefixShown,
                0,
                {
                    GlobalArgType.ActionType.name: AssignedValue("desc", ArgSource.ExplicitPosArg),
                    ServiceArgType.AccessType.name: None,
                },
                "Incomplete token (pointed by the cursor) is complete in invocation mode",
            ),
            (
                line_no(), RunMode.CompletionMode, "some_command goto |", CompType.PrefixShown,
                0,
                {
                    GlobalArgType.ActionType.name: AssignedValue("goto", ArgSource.ExplicitPosArg),
                    GlobalArgType.ObjectSelector.name: None,
                },
                "Explicit assignment for complete token",
            ),
            (
                line_no(), RunMode.CompletionMode, "some_command goto service |", CompType.PrefixShown,
                0,
                {
                    GlobalArgType.ActionType.name: AssignedValue("goto", ArgSource.ExplicitPosArg),
                    GlobalArgType.ObjectSelector.name: AssignedValue("service", ArgSource.ExplicitPosArg),
                },
                "Explicit assignment for complete token",
            ),
            (
                line_no(), RunMode.CompletionMode, "some_command goto host prod|", CompType.PrefixShown,
                1,
                {
                    ServiceArgType.CodeMaturity.name: None,
                    ServiceArgType.AccessType.name: None,
                },
                "No implicit assignment for incomplete token",
            ),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            # (
            #     line_no(), RunMode.InvocationMode, "some_command goto host prod|", CompType.PrefixShown,
            #     1,
            #     {
            #         ServiceArgType.CodeMaturity.name: AssignedValue("prod", ArgSource.ExplicitPosArg),
            #         ServiceArgType.AccessType.name: AssignedValue("ro", ArgSource.ImplicitValue),
            #     },
            #     "Implicit assignment even for incomplete token (token pointed by cursor)",
            # ),
            (
                line_no(), RunMode.CompletionMode, "some_command goto host prod |", CompType.PrefixShown,
                1,
                {
                    ServiceArgType.CodeMaturity.name: AssignedValue("prod", ArgSource.ExplicitPosArg),
                    ServiceArgType.AccessType.name: None,
                },
                "No implicit assignment of access type to \"ro\" when code maturity is \"prod\" in completion",
            ),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            # (
            #     line_no(), RunMode.InvocationMode, "some_command goto host prod |", CompType.PrefixShown,
            #     1,
            #     {
            #         ServiceArgType.CodeMaturity.name: AssignedValue("prod", ArgSource.ExplicitPosArg),
            #         ServiceArgType.AccessType.name: AssignedValue("ro", ArgSource.ImplicitValue),
            #     },
            #     "Implicit assignment of access type to \"ro\" when code maturity is \"prod\" in invocation",
            # ),
            (
                line_no(), RunMode.CompletionMode, "some_command goto host dev |", CompType.PrefixShown,
                1,
                {
                    ServiceArgType.CodeMaturity.name: AssignedValue("dev", ArgSource.ExplicitPosArg),
                    ServiceArgType.AccessType.name: None,
                },
                "No implicit assignment of access type to \"rw\" when code maturity is \"dev\" in completion",
            ),
            # TODO: re-implement functionality via data - see `CodeMaturityProcessor`:
            # (
            #     line_no(), RunMode.InvocationMode, "some_command goto host dev |", CompType.PrefixShown,
            #     1,
            #     {
            #         ServiceArgType.CodeMaturity.name: AssignedValue("dev", ArgSource.ExplicitPosArg),
            #         ServiceArgType.AccessType.name: AssignedValue("rw", ArgSource.ImplicitValue),
            #     },
            #     "Implicit assignment of access type to \"rw\" when code maturity is \"uat\" in invocation",
            # ),
        ]
        # @formatter:on

        for test_case in test_cases:

            with self.subTest(test_case):
                (
                    line_number,
                    run_mode,
                    test_line,
                    comp_type,
                    found_envelope_ipos,
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
                    .set_test_data_ids_to_load([
                        "TD_63_37_05_36",  # demo
                    ])
                )
                with env_mock_builder.build():
                    command_obj = __main__.main()
                    assert isinstance(command_obj, AbstractLocalClientCommand)
                    interp_ctx = command_obj.interp_ctx

                    for arg_type, arg_value in expected_assignments.items():
                        if arg_value is None:
                            self.assertTrue(
                                arg_type not in
                                interp_ctx.envelope_containers
                                [found_envelope_ipos].assigned_types_to_values
                            )
                        else:
                            self.assertEqual(
                                arg_value,
                                interp_ctx.envelope_containers
                                [found_envelope_ipos].assigned_types_to_values
                                [arg_type]
                            )

    def test_capture_invocation_input(self):
        test_line = "some_command goto service prod wert-pd-1 |"
        (command_line, cursor_cpos) = parse_line_and_cpos(test_line)
        env_mock_builder = (
            EnvMockBuilder()
            .set_run_mode(RunMode.InvocationMode)
            .set_command_line(command_line)
            .set_cursor_cpos(cursor_cpos)
            .set_comp_type(CompType.InvokeAction)
            .set_test_data_ids_to_load([
                "TD_63_37_05_36",  # demo
            ])
            .set_capture_invocator_invocation_input(ErrorInvocator)
        )
        with env_mock_builder.build():
            __main__.main()
            print(EnvMockBuilder.invocation_input)
            invocation_input = EnvMockBuilder.invocation_input
            self.assertEqual(
                ServiceEnvelopeClass.ClassService.name,
                invocation_input.data_envelopes[2][ReservedArgType.EnvelopeClass.name]
            )
            self.assertEqual(
                "prod-apac-downstream",
                invocation_input.data_envelopes[2][ServiceArgType.ClusterName.name]
            )
            self.assertEqual(
                "wert-pd-1",
                invocation_input.data_envelopes[2][ServiceArgType.HostName.name]
            )
            self.assertEqual(
                "tt1",
                invocation_input.data_envelopes[2][ServiceArgType.ServiceName.name]
            )
            self.assertTrue(True)
