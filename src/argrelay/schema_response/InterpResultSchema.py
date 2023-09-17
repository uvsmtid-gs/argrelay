from marshmallow import Schema, RAISE, fields, pre_dump, post_load

from argrelay.misc_helper.TypeDesc import TypeDesc
from argrelay.schema_response.EnvelopeContainerSchema import envelope_container_desc
from argrelay.schema_response.InterpResult import InterpResult

"""
Schema for the result of interpretation taken from :class:`InterpContext`
"""

all_tokens_ = "all_tokens"
consumed_tokens_ = "consumed_tokens"
envelope_containers_ = "envelope_containers"
tan_token_ipos_ = "tan_token_ipos"
tan_token_l_part_ = "tan_token_l_part"


class InterpResultSchema(Schema):
    """
    See also `InterpResult`.
    """

    class Meta:
        unknown = RAISE
        ordered = True

    all_tokens = fields.List(
        fields.String(),
        required = True,
    )

    consumed_tokens = fields.List(
        fields.Integer(),
        required = True,
    )

    envelope_containers = fields.List(
        fields.Nested(envelope_container_desc.dict_schema),
        required = True,
    )

    tan_token_ipos = fields.Integer()

    tan_token_l_part = fields.String()

    @pre_dump
    def make_dict(self, input_object: InterpResult, **kwargs):
        if isinstance(input_object, InterpResult):
            return {
                all_tokens_: input_object.all_tokens,
                consumed_tokens_: input_object.consumed_tokens,
                envelope_containers_: input_object.envelope_containers,
                tan_token_ipos_: input_object.tan_token_ipos,
                tan_token_l_part_: input_object.tan_token_l_part,
            }
        else:
            # Assuming it is as dict:
            return input_object
        pass

    @post_load
    def make_object(self, input_dict, **kwargs):
        return InterpResult(
            all_tokens = input_dict[all_tokens_],
            consumed_tokens = input_dict[consumed_tokens_],
            envelope_containers = input_dict[envelope_containers_],
            tan_token_ipos = input_dict[tan_token_ipos_],
            tan_token_l_part = input_dict[tan_token_l_part_],
        )


interp_result_desc = TypeDesc(
    dict_schema = InterpResultSchema(),
    ref_name = InterpResultSchema.__name__,
    dict_example = {
        all_tokens_: [
            "some_command",
            "unrecognized_token",
            "goto",
            "host",
            "prod",
        ],
        consumed_tokens_: [
            0,
            2,
            3,
            4,
        ],
        envelope_containers_: [
            envelope_container_desc.dict_example,
        ],
        tan_token_ipos_: 1,
        tan_token_l_part_: "unrecognized_",
    },
    default_file_path = "",
)
