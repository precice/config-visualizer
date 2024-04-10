import types
import pytest
import glob

from preciceconfigvisualizer.common import configFileToDotCode

VISIBILITY = ["full", "merged", "none"]
TOOGLED = [True, False]
OUTPUT_CONFIGS = [
    types.SimpleNamespace(
        data_access=da,
        data_exchange=de,
        communicators=com,
        cplschemes=cpl,
        mappings=map,
        no_watchpoints=watch,
        no_colors=color,
        margin=10,
    )
    for da in VISIBILITY
    for de in VISIBILITY
    for com in VISIBILITY
    for cpl in VISIBILITY
    for map in VISIBILITY
    for watch in TOOGLED
    for color in TOOGLED
]


@pytest.mark.parametrize(
    "filename, args",
    [(f, a) for f in glob.glob("samples/v*/*.xml") for a in OUTPUT_CONFIGS],
)
def test_dot_from_xml(filename, args):
    assert configFileToDotCode(filename, args) is not None
