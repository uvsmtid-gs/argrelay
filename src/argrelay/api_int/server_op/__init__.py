"""
This package "hides" definition of `relay_server` operations from `relay_client`.
While `relay_client` is supposed to rely on these definitions (and they are often used at test-time),
it is not required to load them at run-time (hence, they are "hidden" in this package).
"""

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from argrelay.api_int.const_int import DEFAULT_OPEN_API_VERSION, UNUSED_TITLE, UNUSED_VERSION
from argrelay.api_int.data_schema.ArgValuesSchema import arg_values_desc
from argrelay.api_int.data_schema.RequestContextSchema import request_context_desc

# This spec is only used to generate data schemas: Marshmallow Schemas -> JSON Schemas.
# These data schemas are subsequently used in OAS specs for paths (which are defined manually).
# All serialization/deserialization/validation is done using Marshmallow Schemas (instead of JSON Schemas).
server_op_data_schemas = APISpec(
    title = UNUSED_TITLE,
    version = UNUSED_VERSION,
    openapi_version = DEFAULT_OPEN_API_VERSION,
    plugins = [MarshmallowPlugin()],
)

# Generate data schemas: Marshmallow Schema -> JSON Schema:
server_op_data_schemas.components.schema(
    request_context_desc.ref_name,
    schema = request_context_desc.object_schema,
)
server_op_data_schemas.components.schema(
    arg_values_desc.ref_name,
    schema = arg_values_desc.object_schema,
)

# Run API docs UI at the root:
API_DOCS_UI_PATH = "/"