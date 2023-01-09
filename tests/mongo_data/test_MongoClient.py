from unittest import TestCase, skip

from pymongo.collection import Collection
from pymongo.database import Database

from argrelay.mongo_data.MongoClientWrapper import get_mongo_client
from argrelay.relay_demo.ServiceArgType import ServiceArgType
from argrelay.schema_config_core_server.MongoConfigSchema import mongo_config_desc
from argrelay.schema_config_core_server.StaticDataSchema import types_to_values_, data_envelopes_


class ThisTestCase(TestCase):

    @staticmethod
    def show_all_envelopes(col_proxy: Collection):
        print("show_all_envelopes:")
        for data_envelope in col_proxy.find():
            print("data_envelope: ", data_envelope)

    @staticmethod
    def remove_all_envelopes(col_proxy):
        col_proxy.delete_many({})

    # noinspection PyMethodMayBeStatic
    @skip  # test again running server
    def test_live_tutorial(self):
        """
        Inspired by: https://www.mongodb.com/languages/python
        """

        mongo_config = mongo_config_desc.from_input_dict(mongo_config_desc.dict_example)
        mongo_client = get_mongo_client(mongo_config)
        print("list_database_names: ", mongo_client.list_database_names())

        mongo_db: Database = mongo_client[mongo_config.database_name]
        print("list_collection_names: ", mongo_db.list_collection_names())

        col_name = "user_1_envelopes"
        col_proxy: Collection = mongo_db[col_name]

        self.show_all_envelopes(col_proxy)

        self.remove_all_envelopes(col_proxy)

        envelope_1 = {
            "_id": "U1IT00001",
            "envelope_name": "Blender",
            "max_discount": "10%",
            "batch_number": "RR450020FRG",
            "price": 340,
            "category": "kitchen appliance",
        }

        envelope_2 = {
            "_id": "U1IT00002",
            "envelope_name": "Egg",
            "category": "food",
            "quantity": 12,
            "price": 36,
            "envelope_description": "brown country eggs",
        }

        envelope_3 = {
            "envelope_name": "whatever",
            "category": "whatever",
            "batch_number": "whatever",
            "price": 999,
        }

        envelope_4 = {
            "envelope_name": "butter",
            "category": "food",
            "batch_number": "BU5E0020FK",
            "price": 20,
        }

        envelope_5 = {
            "envelope_name": "face cream",
            "category": "beauty",
            "max_discount": "4%",
            "ingredients": "Hyaluronic acid, Ceramides, vitamins A,C,E, fruit acids",
        }

        envelope_6 = {
            "envelope_name": "fishing plier",
            "category": "sports",
            "envelope_description": "comes with tungsten carbide cutters to easily cut fishing lines and hooks",
        }

        envelope_7 = {
            "envelope_name": "pizza sauce",
            "category": "food",
            "quantity": 5,
        }

        envelope_8 = {
            "envelope_name": "fitness band",
            "price": 300,
            "max_discount": "12%",
        }

        envelope_9 = {
            "envelope_name": "cinnamon",
            "category": "food",
            "warning": "strong smell, not to be consumed directly",
            "price": 2,
        }

        envelope_10 = {
            "envelope_name": "lego building set",
            "category": "toys",
            "warning": "very small parts, not suitable for children below 3 years",
            "parts_included": "colored interlocking plastic bricks, gears, minifigures, plates, cones, round bricks",
        }

        envelope_11 = {
            "envelope_name": "dishwasher",
            "category": "kitchen appliance",
            "warranty": "2 years",
        }

        envelope_12 = {
            "envelope_name": "running shoes",
            "brand": "Nike",
            "category": "sports",
            "price": 145,
            "max_discount": "5%",
        }

        envelope_13 = {
            "envelope_name": "leather bookmark",
            "category": "books",
            "design": "colored alphabets",
            "envelope_description": "hand-made, natural colors used",
        }

        envelope_14 = {
            "envelope_name": "maple syrup",
            "category": "food",
            "envelope_description": "A-grade, dark, organic, keep in refrigerator after opening",
            "price": 25,
        }

        col_proxy.insert_many([
            envelope_1,
            envelope_2,
            envelope_3,
            envelope_4,
            envelope_5,
            envelope_6,
            envelope_7,
            envelope_8,
            envelope_9,
            envelope_10,
            envelope_11,
            envelope_12,
            envelope_13,
            envelope_14,
        ])

        col_proxy.create_index("category")

    # noinspection PyMethodMayBeStatic
    @skip  # test again running server
    def test_live_envelope_searched_by_multiple_typed_vals(self):
        """
        Example with data searched by multiple { type: value } pairs
        """

        mongo_config = mongo_config_desc.from_input_dict(mongo_config_desc.dict_example)
        mongo_client = get_mongo_client(mongo_config)
        print("list_database_names: ", mongo_client.list_database_names())

        mongo_db: Database = mongo_client[mongo_config.database_name]
        print("list_collection_names: ", mongo_db.list_collection_names())

        col_name = "argrelay"
        col_proxy: Collection = mongo_db[col_name]

        self.remove_all_envelopes(col_proxy)

        envelope_001 = {
            "envelope_payload": {
                "object_name": "envelope_001",
            },
            types_to_values_: {
                ServiceArgType.AccessType.name: "ro",
            },
        }

        envelope_002 = {
            "envelope_payload": {
                "object_name": "envelope_002",
            },
            types_to_values_: {
                ServiceArgType.AccessType.name: "rw",
                ServiceArgType.ColorTag.name: "red",
            },
        }

        envelope_003 = {
            "envelope_payload": {
                "object_name": "envelope_003",
            },
            types_to_values_: {
                ServiceArgType.AccessType.name: "rw",
                ServiceArgType.ColorTag.name: "blue",
            },
        }

        envelope_004 = {
            "envelope_payload": {
                "object_name": "envelope_004",
            },
            types_to_values_: {
                ServiceArgType.AccessType.name: "rw",
                ServiceArgType.ColorTag.name: "red",
                ServiceArgType.CodeMaturity.name: "prod",
            },
        }

        col_proxy.insert_many([
            envelope_001,
            envelope_002,
            envelope_003,
            envelope_004,
        ])

        col_proxy.create_index(types_to_values_)

        print("query 1:")
        for data_envelope in col_proxy.find(
            {
                f"types_to_values.{ServiceArgType.AccessType.name}": "rw",
                f"types_to_values.{ServiceArgType.ColorTag.name}": "red",
            }
        ):
            print("data_envelope: ", data_envelope)

        self.remove_all_envelopes(col_proxy)

    @skip  # test again running server
    def test_list_all_envelopes(self):
        """
        Does not test anything, just lists envelopes in current database collection:
        """

        mongo_config = mongo_config_desc.from_input_dict(mongo_config_desc.dict_example)
        mongo_client = get_mongo_client(mongo_config)
        print("list_database_names: ", mongo_client.list_database_names())

        mongo_db: Database = mongo_client[mongo_config.database_name]
        print("list_collection_names: ", mongo_db.list_collection_names())

        col_name = data_envelopes_
        col_proxy: Collection = mongo_db[col_name]

        self.show_all_envelopes(col_proxy)
