from gedcom.element.element import Element
from gedcom.element.submitter import SubmitterElement
import gedcom.tags


def test_initialization():
    submitter_element = SubmitterElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_SUBMITTER, value="")
    assert isinstance(submitter_element, Element)
    assert isinstance(submitter_element, SubmitterElement)
