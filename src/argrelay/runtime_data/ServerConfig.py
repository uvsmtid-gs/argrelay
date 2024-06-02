from __future__ import annotations

from dataclasses import dataclass, field

from argrelay.enum_desc.PluginType import PluginType
from argrelay.mongo_data.MongoConfig import MongoConfig
from argrelay.relay_server.GuiBannerConfig import GuiBannerConfig
from argrelay.relay_server.QueryCacheConfig import QueryCacheConfig
from argrelay.runtime_data.ConnectionConfig import ConnectionConfig
from argrelay.runtime_data.ServerPluginControl import ServerPluginControl
from argrelay.runtime_data.StaticData import StaticData
from argrelay.schema_config_plugin.PluginEntrySchema import plugin_enabled_, plugin_dependencies_


@dataclass
class ServerConfig:
    connection_config: ConnectionConfig = field()
    mongo_config: MongoConfig = field()
    query_cache_config: QueryCacheConfig = field()
    gui_banner_config: GuiBannerConfig = field()
    class_to_collection_map: dict = field()
    server_plugin_control: ServerPluginControl = field()

    # TODO_00_79_72_55: remove in the future:
    static_data: StaticData = field()

    # TODO: Keep this runtime objects in separate (`ServerRuntime`?) class. Ensure/implement ServerConfig dumping on request (for troubleshooting).
    data_loaders: dict[str, "AbstractLoader"] = field(default_factory = lambda: {})
    """
    Entries in `data_loaders` are not directly loaded from config.
    These are plugin instances created during plugin activation.
    """

    # TODO: Keep this runtime objects in separate (`ServerRuntime`?) class. Ensure/implement ServerConfig dumping on request (for troubleshooting).
    interp_factories: dict[str, "AbstractInterpFactory"] = field(default_factory = lambda: {})
    """
    Entries in `interp_factories` are not directly loaded from config.
    These are plugin instances created during plugin activation.
    """

    # TODO: Keep this runtime objects in separate (`ServerRuntime`?) class. Ensure/implement ServerConfig dumping on request (for troubleshooting).
    action_delegators: dict[str, "AbstractDelegator"] = field(default_factory = lambda: {})
    """
    Entries in `action_delegators` are not directly loaded from config.
    These are plugin instances created during plugin activation.
    """

    # TODO: Keep this runtime objects in separate (`ServerRuntime`?) class. Ensure/implement ServerConfig dumping on request (for troubleshooting).
    server_configurators: dict[str, "AbstractConfigurator"] = field(default_factory = lambda: {})


# TODO: move to PluginConfig:
def assert_plugin_instance_id(
    server_config: ServerConfig,
    plugin_instance_id: str,
    plugin_type: PluginType,
):
    error_msg = f"plugin instance `{plugin_instance_id}` must: (A) be `{PluginType.DelegatorPlugin.name}`, (B) be `{plugin_enabled_}`, (C) be activated in the order of DAG via `{plugin_dependencies_}`"
    if plugin_type is PluginType.InterpFactoryPlugin:
        assert plugin_instance_id in server_config.interp_factories, error_msg
    if plugin_type is PluginType.DelegatorPlugin:
        assert plugin_instance_id in server_config.action_delegators, error_msg
    if plugin_type is PluginType.LoaderPlugin:
        assert plugin_instance_id in server_config.data_loaders, error_msg
