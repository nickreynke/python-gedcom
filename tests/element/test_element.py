from gedcom.element.element import Element


def test_initialization():
    element = Element(level=-1, pointer="", tag="", value="")
    assert isinstance(element, Element)

def _build_simple_individual():
    element = Element(level=0, pointer="@I5@", tag="INDI", value="")
    name = element.new_child_element(tag="NAME", value="First /Last/")
    sex = element.new_child_element(tag="SEX", value="M")
    birth = element.new_child_element(tag="BIRT", value="")
    birth_date = birth.new_child_element(tag="DATE", value="1 JAN 1900")
    birth_place = birth.new_child_element(tag="PLAC", value="Pacific Ocean, Washington, USA")
    birth_place_map = birth_place.new_child_element(tag="MAP", value="")
    birth_place_map.new_child_element(tag="LATI", value="N47.680663")
    birth_place_map.new_child_element(tag="LONG", value="W122.234319")
    return element

def test_to_gedcom_string():
    element = _build_simple_individual()
    assert element.to_gedcom_string(recursive=False) == "0 @I5@ INDI\n"

def test_to_gedcom_string_recursive():
    element = _build_simple_individual()
    assert element.to_gedcom_string(recursive=True) == """0 @I5@ INDI
1 NAME First /Last/
1 SEX M
1 BIRT
2 DATE 1 JAN 1900
2 PLAC Kirkland, King, Washington, USA
3 MAP
4 LATI N47.680663
4 LONG W122.234319
"""
