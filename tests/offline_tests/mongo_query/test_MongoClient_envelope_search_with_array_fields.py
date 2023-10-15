from __future__ import annotations

from icecream import ic
from pymongo.collection import Collection

from argrelay.custom_integ.ServiceArgType import ServiceArgType
from argrelay.schema_config_interp.DataEnvelopeSchema import envelope_payload_
from offline_tests.mongo_query.MongoClientTest import MongoClientTestCase, object_name_


class ThisTestCase(MongoClientTestCase):

    # noinspection PyMethodMayBeStatic
    def test_live_envelope_searched_by_multiple_typed_key_value_pairs(self):
        """
        Example with data searched by multiple { type: value } pairs
        where some fields contain array of values.
        See: FS_06_99_43_60.list_arg_value.md
        """

        # Fields which will be indexed:
        known_arg_types = [
            ServiceArgType.AccessType.name,
            ServiceArgType.LiveStatus.name,
            ServiceArgType.CodeMaturity.name,
        ]

        envelope_001 = {
            envelope_payload_: {
                object_name_: "envelope_001",
            },
            ServiceArgType.AccessType.name: "ro",
        }

        envelope_002 = {
            envelope_payload_: {
                object_name_: "envelope_002",
            },
            ServiceArgType.AccessType.name: "rw",
            ServiceArgType.LiveStatus.name: [
                "red",
                "blue",
            ],
        }

        envelope_003 = {
            envelope_payload_: {
                object_name_: "envelope_003",
            },
            ServiceArgType.AccessType.name: "rw",
            # NOTE: some of the envelopes have scalar value for the same field which has arrays in other envelopes:
            ServiceArgType.LiveStatus.name: "blue",
        }

        envelope_004 = {
            envelope_payload_: {
                object_name_: "envelope_004",
            },
            ServiceArgType.AccessType.name: "rw",
            ServiceArgType.LiveStatus.name: [
                "red",
                "yellow",
            ],
            ServiceArgType.CodeMaturity.name: "prod",
        }

        envelope_005 = {
            envelope_payload_: {
                object_name_: "envelope_005",
            },
            ServiceArgType.AccessType.name: "rw",
            ServiceArgType.LiveStatus.name: [
                "blue",
                "green",
            ],
            ServiceArgType.CodeMaturity.name: "prod",
        }

        envelope_006 = {
            envelope_payload_: {
                object_name_: "envelope_006",
            },
            ServiceArgType.AccessType.name: "rw",
            # NOTE: some of the envelopes have scalar value for the same field which has arrays in other envelopes:
            ServiceArgType.LiveStatus.name: "green",
            ServiceArgType.CodeMaturity.name: "prod",
        }

        envelope_007 = {
            envelope_payload_: {
                object_name_: "envelope_007",
            },
            ServiceArgType.AccessType.name: "rw",
            ServiceArgType.LiveStatus.name: [
                "red",
                "green",
                "blue",
                "yellow",
            ],
            ServiceArgType.CodeMaturity.name: "prod",
        }

        self.col_proxy.insert_many([
            envelope_001,
            envelope_002,
            envelope_003,
            envelope_004,
            envelope_005,
            envelope_006,
            envelope_007,
        ])

        self.index_fields(self.col_proxy, known_arg_types)

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: "red",
            }),
            [
                "envelope_002",
                "envelope_004",
                "envelope_007",
            ],
        )

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: "yellow",
            }),
            [
                "envelope_004",
                "envelope_007",
            ],
        )

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: "blue",
            }),
            [
                "envelope_002",
                "envelope_003",
                "envelope_005",
                "envelope_007",
            ],
        )

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: "green",
            }),
            [
                "envelope_005",
                "envelope_006",
                "envelope_007",
            ],
        )

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: [
                    "green",
                    "blue",
                ]
            }),
            # NOTE: query with array of values does not work:
            [
            ],
        )

        self.find_and_assert(
            self.col_proxy,
            ic({
                ServiceArgType.LiveStatus.name: [
                    "green",
                    "blue",
                ]
            }),
            # NOTE: query with array of values does not work:
            [
            ],
        )

        self.remove_all_data(self.col_proxy)

    def find_and_assert(
        self,
        col_proxy: Collection,
        query_dict: dict,
        expected_object_names: list[str],
    ):
        data_envelopes = list(col_proxy.find(query_dict))
        for data_envelope in data_envelopes:
            ic(data_envelope)
        self.assertTrue(len(data_envelopes) == len(expected_object_names))
        actual_object_names = self.extract_object_names(data_envelopes)
        for expected_object_name in expected_object_names:
            self.assertTrue(expected_object_name in actual_object_names)

    @staticmethod
    def extract_object_names(
        data_envelopes: list[dict],
    ):
        return [data_envelope[envelope_payload_][object_name_] for data_envelope in data_envelopes]
