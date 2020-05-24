from gedcom.element.element import Element
from gedcom.element.source import SourceElement
import gedcom.tags


def test_initialization():
    source_element = SourceElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_SOURCE, value="")
    assert isinstance(source_element, Element)
    assert isinstance(source_element, SourceElement)
