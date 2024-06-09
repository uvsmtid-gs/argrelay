from argrelay.custom_integ.ServicePropName import ServicePropName
from argrelay.schema_config_interp.DataEnvelopeSchema import envelope_payload_, mongo_id_
from offline_tests.mongo_query.MongoClientTestClass import MongoClientTestClass, object_name_


class ThisTestClass(MongoClientTestClass):

    # noinspection PyMethodMayBeStatic
    def test_live_query_distinct_values_for_each_indexed_field(self):
        """
        Example to search distinct values for each field individually in single query:
        https://stackoverflow.com/a/63595331/441652
        """

        index_fields = [
            ServicePropName.access_type.name,
            ServicePropName.live_status.name,
            ServicePropName.code_maturity.name,
        ]

        envelope_001 = {
            envelope_payload_: {
                object_name_: "envelope_001",
            },
            ServicePropName.access_type.name: "ro",
            ServicePropName.code_maturity.name: "prod",
        }

        envelope_002 = {
            envelope_payload_: {
                object_name_: "envelope_002",
            },
            ServicePropName.access_type.name: "rw",
            ServicePropName.live_status.name: "red",
        }

        envelope_003 = {
            envelope_payload_: {
                object_name_: "envelope_003",
            },
            ServicePropName.access_type.name: "rw",
            ServicePropName.live_status.name: "blue",
        }

        envelope_004 = {
            envelope_payload_: {
                object_name_: "envelope_004",
            },
            ServicePropName.access_type.name: "rw",
            ServicePropName.live_status.name: "red",
            ServicePropName.code_maturity.name: "prod",
        }

        self.col_proxy.insert_many([
            envelope_001,
            envelope_002,
            envelope_003,
            envelope_004,
        ])

        self.index_fields(self.col_proxy, index_fields)

        print("query 1:")
        for result_item in self.col_proxy.aggregate([
            {
                "$group": {
                    mongo_id_: None,
                    ServicePropName.access_type.name: {
                        "$addToSet": f"${ServicePropName.access_type.name}"
                    },
                    ServicePropName.live_status.name: {
                        "$addToSet": f"${ServicePropName.live_status.name}"
                    },
                    ServicePropName.code_maturity.name: {
                        "$addToSet": f"${ServicePropName.code_maturity.name}"
                    },
                },
            },
        ]):
            print("result_item: ", result_item)
