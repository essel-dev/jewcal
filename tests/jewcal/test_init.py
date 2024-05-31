# type: ignore
"""Unittests for jewcal __init__.

__init__.py contains doctests for documentation (tutorials).
"""

from doctest import NORMALIZE_WHITESPACE, DocTestSuite


def load_tests(loader, tests, ignore):  # pylint: disable=unused-argument
    """Run the doctests in jewcal.__init__.py.

    # noqa: DAR101 loader
    # noqa: DAR101 tests
    # noqa: DAR101 ignore
    # noqa: DAR201 return
    """
    tests.addTests(
        DocTestSuite('src.jewcal.__init__', optionflags=NORMALIZE_WHITESPACE)
    )
    return tests
