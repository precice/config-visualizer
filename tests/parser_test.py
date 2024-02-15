import unittest

from preciceconfigvisualizer.common import parseXMLFile


class ParseTests(unittest.TestCase):
    def test_v2_solverdummy(self):
        self.assertIsNotNone(parseXMLFile("samples/v2/solverdummy.xml"))

    def test_v2_generated(self):
        self.assertIsNotNone(parseXMLFile("samples/v2/generated.xml"))

    def test_v3_solverdummy(self):
        self.assertIsNotNone(parseXMLFile("samples/v3/solverdummy.xml"))
