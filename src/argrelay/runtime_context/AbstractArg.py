"""
This module lists interfaces for various args.
"""

from __future__ import annotations


class AbstractArg:
    """
    An arg of any origin (env, config, command) which can be used for a func.
    """


class ArgCommand(AbstractArg):
    """
    Represents `command_arg` - see FS_27_16_67_19 line syntax
    """

    def get_arg_tokens(
        self,
    ) -> list[int]:
        return []


class ArgCommandValue(ArgCommand):
    """
    Represents any `command_arg` with value.
    """

    def get_arg_value(
        self
    ) -> str:
        raise NotImplementedError


class ArgCommandValueOffered(ArgCommandValue):
    """
    Represents FS_96_46_42_30 `offered_arg`.
    """


class ArgCommandValueDictated(ArgCommandValue):
    """
    Represents FS_20_88_05_60 `dictated_arg`.
    """

    def get_arg_name(
        self
    ) -> str:
        raise NotImplementedError
