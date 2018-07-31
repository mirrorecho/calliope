import abjad
import pytest
import calliope

@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
	doctest_namespace["abjad"] = abjad
	doctest_namespace["calliope"] = calliope