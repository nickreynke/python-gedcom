from gedcom.element.element import Element
from gedcom.element.header import HeaderElement
import gedcom.tags


def test_initialization():
    header_element = HeaderElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_HEADER, value="")
    assert isinstance(header_element, Element)
    assert isinstance(header_element, HeaderElement)
