import os

from marshmallow import Schema, RAISE, fields, post_load

from argrelay.data_schema.ConnectionConfigSchema import connection_config_desc
from argrelay.meta_data.ClientConfig import ClientConfig
from argrelay.misc_helper.TypeDesc import TypeDesc

connection_config_ = "connection_config"
use_local_requests_ = "use_local_requests"


class ClientConfigSchema(Schema):
    class Meta:
        unknown = RAISE
        strict = True

    # Serve requests from local data or send to server:
    use_local_requests = fields.Boolean()
    connection_config = fields.Nested(connection_config_desc.object_schema)

    @post_load
    def make_object(self, input_dict, **kwargs):
        return ClientConfig(
            use_local_requests = input_dict[use_local_requests_],
            connection_config = input_dict[connection_config_],
        )


client_config_desc = TypeDesc(
    object_schema = ClientConfigSchema(),
    ref_name = ClientConfigSchema.__name__,
    dict_example = {
        use_local_requests_: False,
        connection_config_: connection_config_desc.dict_example,
    },
    default_file_path = os.path.expanduser("~") + "/" + ".argrelay.client.yaml",
)