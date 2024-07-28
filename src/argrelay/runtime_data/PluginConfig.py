from __future__ import annotations

from dataclasses import dataclass, field

from argrelay.runtime_data.PluginEntry import PluginEntry


@dataclass
class PluginConfig:
    """
    See also `PluginConfigSchema`.
    """

    reusable_config_data: dict = field()
    """
    Arbitrary data
    """

    plugin_instance_entries: dict[str, PluginEntry] = field()
    """
    Key = `plugin_instance_id`
    """

    plugin_instance_id_activate_list: list[str] = field()
    """
    List of `plugin_instance_id`-s in order of activation generated by
    walking through a DAG described by `plugin_dependencies`.
    Each `plugin_instance_id` is a key into `plugin_instance_entries`.
    """

    # TODO: Move it into separate file/object:
    check_env_plugin_instance_entries: dict[str, PluginEntry] = field()
    """
    Same as `plugin_instance_entries` but for FS_36_17_84_44 `check_env` only.
    """

    # TODO: Move it into separate file/object:
    check_env_plugin_instance_id_activate_list: list[str] = field()
    """
    Same as `plugin_instance_id_activate_list` but for FS_36_17_84_44 `check_env` only.
    """
