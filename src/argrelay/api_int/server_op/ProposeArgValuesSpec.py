from argrelay.api_int.data_schema.ArgValuesSchema import arg_values_desc
from argrelay.api_int.data_schema.RequestContextSchema import request_context_desc
from argrelay.api_int.server_op import server_op_data_schemas

spec_data = {
    "parameters": [
        {
            "name": request_context_desc.ref_name,
            "in": "body",
            "description": "propose arg values for given command line and cursor position",
            "required": True,
            "schema": {
                "$ref": "#/definitions/" + request_context_desc.ref_name,
            },
            "example": request_context_desc.dict_example,
        },
    ],
    "responses": {
        "200": {
            "schema": {
                "$ref": "#/definitions/" + arg_values_desc.ref_name,
            },
        },
    },
    "definitions": {
        request_context_desc.ref_name: server_op_data_schemas.components.schemas[request_context_desc.ref_name],
        arg_values_desc.ref_name: server_op_data_schemas.components.schemas[arg_values_desc.ref_name],
    },
}