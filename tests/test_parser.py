from gedcom.element.individual import IndividualElement
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
    gedcom_parser.parse([(a + '\n') for a in case_1.splitlines()])
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
    gedcom_parser.parse([(a + '\n') for a in case_2.splitlines()])
    element_2 = gedcom_parser.get_root_child_elements()[0]
    assert element_2.get_tag() == 'FAM'
    assert element_2.get_pointer() == '@F28@'
    element_2_children = element_2.get_child_elements()
    assert len(element_2_children) == 5
    assert element_2_children[0].get_tag() == 'HUSB'
    assert element_2_children[1].get_tag() == 'WIFE'
    assert element_2_children[2].get_tag() == 'CHIL'
    assert element_2_children[3].get_value() == '@I84@'


def test_to_gedcom_string():
    # From string
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
    gedcom_parser.parse([(a + '\n') for a in case_1.splitlines()])

    case_1_string_array = case_1.splitlines()
    gedcom_string = gedcom_parser.to_gedcom_string(True)
    gedcom_string_array = gedcom_string.splitlines()

    # Check number of lines
    assert len(case_1_string_array) == len(gedcom_string_array) == 9

    # Check each line
    for i in range(len(case_1_string_array)):
        assert case_1_string_array[i] == gedcom_string_array[i]

    # Check whole file string
    assert gedcom_string == case_1

    # From file
    case_2 = ""

    with open('tests/files/Musterstammbaum.ged', 'rb') as gedcom_stream:
        for line in gedcom_stream:
            case_2 += line.decode('utf-8-sig')

    gedcom_parser.parse_file('tests/files/Musterstammbaum.ged')

    case_2_string_array = case_2.splitlines()
    gedcom_string = gedcom_parser.to_gedcom_string(True)
    gedcom_string_array = gedcom_string.splitlines()

    # Check number of lines
    assert len(case_2_string_array) == len(gedcom_string_array) == 396

    # Check each line
    for i in range(len(case_2_string_array)):
        assert case_2_string_array[i] == gedcom_string_array[i]

    # Check whole file string
    assert gedcom_string == case_2


def test___parse_line():
    # @TODO Add appropriate testing cases
    pass
