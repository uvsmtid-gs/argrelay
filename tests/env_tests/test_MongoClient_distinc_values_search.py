from offline_tests.mongo_query import test_MongoClient_distinc_values_search


class ThisTestCase(test_MongoClient_distinc_values_search.ThisTestCase):
    """
    Reconfigures existing tests to run against real MongoDB.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(
            ThisTestCase,
            self,
        ).__init__(
            *args,
            **kwargs,
        )

        self.use_mongomock_only = False
