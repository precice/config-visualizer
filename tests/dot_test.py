import types
import unittest

from preciceconfigvisualizer.common import configFileToDotCode


class DotTests(unittest.TestCase):
    def setUp(self):
        self.args = types.SimpleNamespace(
            data_access="full",
            data_exchange="full",
            communicators="full",
            cplschemes="full",
            mappings="full",
            no_watchpoints=False,
            no_colors=False,
            margin=10,
        )

    def test_v2_solverdummy(self):
        self.assertIsNotNone(
            configFileToDotCode("samples/v2/solverdummy.xml", self.args)
        )

    def test_v2_generated(self):
        self.assertIsNotNone(configFileToDotCode("samples/v2/generated.xml", self.args))

    def test_v3_solverdummy(self):
        self.assertIsNotNone(
            configFileToDotCode("samples/v3/solverdummy.xml", self.args)
        )
