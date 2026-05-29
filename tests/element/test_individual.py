from gedcom.element.element import Element
from gedcom.element.individual import IndividualElement
import gedcom.tags


def test_initialization():
    individual_element = IndividualElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_INDIVIDUAL, value="")
    assert isinstance(individual_element, Element)
    assert isinstance(individual_element, IndividualElement)


def test_get_all_names():
    element = IndividualElement(level=0, pointer="@I5@", tag="INDI", value="")
    element.new_child_element(tag="NAME", value="First /Last/")
    element.new_child_element(tag="SEX", value="M")
    birth = element.new_child_element(tag="BIRT", value="")
    birth.new_child_element(tag="DATE", value="1 JAN 1900")
    element.new_child_element(tag="NAME", value="Second /Surname/")

    all_names = element.get_all_names()
    assert len(all_names) == 2


def test_deprecated_get_burial_returns_data():
    """Regression test: get_burial() is missing a return statement and returns None instead of the burial tuple."""
    element = IndividualElement(level=0, pointer="@I1@", tag="INDI", value="")
    burial = element.new_child_element(tag=gedcom.tags.GEDCOM_TAG_BURIAL, value="")
    burial.new_child_element(tag=gedcom.tags.GEDCOM_TAG_DATE, value="1 JAN 2000")
    burial.new_child_element(tag=gedcom.tags.GEDCOM_TAG_PLACE, value="Szczecinek")

    result = element.get_burial()

    assert result is not None, "get_burial() returned None — missing return statement bug"
    assert result == ("1 JAN 2000", "Szczecinek", [])


def test_deprecated_get_census_returns_data():
    """Regression test: get_census() is missing a return statement and returns None instead of the census list."""
    element = IndividualElement(level=0, pointer="@I1@", tag="INDI", value="")
    census = element.new_child_element(tag=gedcom.tags.GEDCOM_TAG_CENSUS, value="")
    census.new_child_element(tag=gedcom.tags.GEDCOM_TAG_DATE, value="1 JAN 1950")
    census.new_child_element(tag=gedcom.tags.GEDCOM_TAG_PLACE, value="Szczebrzeszyn")

    result = element.get_census()

    assert result is not None, "get_census() returned None — missing return statement bug"
    assert len(result) == 1
    assert result[0] == ("1 JAN 1950", "Szczebrzeszyn", [])


def test_get_burial_data_returns_data():
    element = IndividualElement(level=0, pointer="@I1@", tag="INDI", value="")
    burial = element.new_child_element(tag=gedcom.tags.GEDCOM_TAG_BURIAL, value="")
    burial.new_child_element(tag=gedcom.tags.GEDCOM_TAG_DATE, value="1 JAN 2000")
    burial.new_child_element(tag=gedcom.tags.GEDCOM_TAG_PLACE, value="Szczecinek")

    result = element.get_burial_data()

    assert result is not None
    assert result == ("1 JAN 2000", "Szczecinek", [])


def test_get_census_data_returns_data():
    element = IndividualElement(level=0, pointer="@I1@", tag="INDI", value="")
    census = element.new_child_element(tag=gedcom.tags.GEDCOM_TAG_CENSUS, value="")
    census.new_child_element(tag=gedcom.tags.GEDCOM_TAG_DATE, value="1 JAN 1950")
    census.new_child_element(tag=gedcom.tags.GEDCOM_TAG_PLACE, value="Szczebrzeszyn")

    result = element.get_census_data()

    assert result is not None
    assert len(result) == 1
    assert result[0] == ("1 JAN 1950", "Szczebrzeszyn", [])
