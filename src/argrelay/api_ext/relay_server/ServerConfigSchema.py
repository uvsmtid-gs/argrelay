import os

from marshmallow import Schema, fields, RAISE, post_load

from argrelay.api_ext.ConnectionConfigSchema import connection_config_desc
from argrelay.api_ext.relay_server.PluginEntrySchema import plugin_entry_desc
from argrelay.api_ext.relay_server.ServerConfig import ServerConfig
from argrelay.api_ext.relay_server.StaticDataSchema import static_data_desc
from argrelay.misc_helper.TypeDesc import TypeDesc
from argrelay.mongo_data.MongoConfigSchema import mongo_config_desc

connection_config_ = "connection_config"
mongo_config_ = "mongo_config"


class ServerConfigSchema(Schema):
    class Meta:
        unknown = RAISE
        strict = True

    connection_config = fields.Nested(
        connection_config_desc.object_schema,
        required = True,
    )
    mongo_config = fields.Nested(
        mongo_config_desc.object_schema,
        required = True,
    )
    plugin_list = fields.List(
        fields.Nested(plugin_entry_desc.object_schema),
        required = True,
    )
    static_data = fields.Nested(
        static_data_desc.object_schema,
        required = True,
    )

    # No interp_factories field for schema - it is generated for ServerConfig internally based on plugin_list.

    @post_load
    def make_object(self, input_dict, **kwargs):
        return ServerConfig(
            connection_config = input_dict[connection_config_],
            mongo_config = input_dict[mongo_config_],
            plugin_list = input_dict["plugin_list"],
            static_data = input_dict["static_data"],
        )


server_config_desc = TypeDesc(
    object_schema = ServerConfigSchema(),
    ref_name = ServerConfigSchema.__name__,
    dict_example = {
        connection_config_: connection_config_desc.dict_example,
        mongo_config_: mongo_config_desc.dict_example,
        "plugin_list": [
            plugin_entry_desc.dict_example,
        ],
        "static_data": static_data_desc.dict_example,
    },
    default_file_path = os.path.expanduser("~") + "/" + ".argrelay.server.yaml",
)
