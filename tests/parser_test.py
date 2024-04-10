import pytest
import glob

from preciceconfigvisualizer.common import parseXMLFile


@pytest.mark.parametrize("filename", glob.glob("samples/v*/*.xml"))
def test_parse_xml(filename):
    assert parseXMLFile(filename) is not None
