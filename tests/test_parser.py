import pytest
from gedcom.element.element import Element
from gedcom.element.individual import IndividualElement, NotAnActualIndividualError
from gedcom.element.root import RootElement
from gedcom.parser import Parser


def test_initialization():
    parser = Parser()
    assert isinstance(parser, Parser)


def test_invalidate_cache():
    parser = Parser()
    parser.parse_file('tests/files/Musterstammbaum.ged')

    assert len(parser.get_element_list()) == 396
    assert len(parser.get_element_dictionary()) == 32

    parser.invalidate_cache()

    assert len(parser.get_element_list()) == 396
    assert len(parser.get_element_dictionary()) == 32


def test_get_root_element():
    parser = Parser()
    assert isinstance(parser.get_root_element(), RootElement)


def test_parse_file():
    parser = Parser()

    assert len(parser.get_root_child_elements()) == 0

    parser.parse_file('tests/files/Musterstammbaum.ged')

    assert len(parser.get_root_child_elements()) == 34

    individuals_in_root_child_elements = 0
    individuals_in_element_list = 0

    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            individuals_in_root_child_elements += 1

    for element in parser.get_element_list():
        if isinstance(element, IndividualElement):
            individuals_in_element_list += 1

    assert individuals_in_root_child_elements == 20
    assert individuals_in_element_list == 20


def test_parse_from_string():
    case_1 = """0 @I5@ INDI
1 NAME First /Last/
1 SEX M
1 BIRT
2 DATE 1 JAN 1900
2 PLAC Kirkland, King, Washington, USA
3 MAP
4 LATI N47.680663
4 LONG W122.234319
"""
    gedcom_parser = Parser()
    gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_1.splitlines()])
    element_1 = gedcom_parser.get_root_child_elements()[0]
    assert isinstance(element_1, IndividualElement)
    assert element_1.get_tag() == 'INDI'
    assert element_1.get_pointer() == '@I5@'
    element_1_children = element_1.get_child_elements()
    assert len(element_1_children) == 3
    assert element_1_children[0].get_tag() == 'NAME'
    assert element_1_children[1].get_tag() == 'SEX'
    assert element_1_children[2].get_tag() == 'BIRT'

    case_2 = """0 @F28@ FAM
1 HUSB @I80@
1 WIFE @I81@
1 CHIL @I9@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I84@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I85@
2 _FREL Natural
2 _MREL Natural
"""
    gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_2.splitlines()])
    element_2 = gedcom_parser.get_root_child_elements()[0]
    assert element_2.get_tag() == 'FAM'
    assert element_2.get_pointer() == '@F28@'
    element_2_children = element_2.get_child_elements()
    assert len(element_2_children) == 5
    assert element_2_children[0].get_tag() == 'HUSB'
    assert element_2_children[1].get_tag() == 'WIFE'
    assert element_2_children[2].get_tag() == 'CHIL'
    assert element_2_children[3].get_value() == '@I84@'


def test___parse_line():
    # @TODO Add appropriate testing cases
    pass


def test_find_path_to_ancestor_raises_for_invalid_ancestor():
    """Regression test for the 'and' vs 'or' bug in find_path_to_ancestor.

    The guard condition uses 'and' instead of 'or', so passing a valid
    descendant with an invalid ancestor silently skips the check and crashes
    later with an AttributeError instead of NotAnActualIndividualError.
    """
    parser = Parser()
    individual = IndividualElement(0, '@I1@', 'INDI', '', '\n')
    non_individual = Element(0, '', 'NOTE', 'some note', '\n')

    # valid descendant, invalid ancestor — the bug lets this slip through
    with pytest.raises(NotAnActualIndividualError):
        parser.find_path_to_ancestor(individual, non_individual)


def test_find_path_to_ancestor_raises_for_both_invalid():
    """Both arguments invalid — the buggy 'and' condition evaluates to False
    and skips the guard entirely, crashing later instead of raising properly.
    """
    parser = Parser()
    non_individual_1 = Element(0, '', 'NOTE', 'some note', '\n')
    non_individual_2 = Element(0, '', 'SOUR', 'some source', '\n')

    with pytest.raises(NotAnActualIndividualError):
        parser.find_path_to_ancestor(non_individual_1, non_individual_2)
