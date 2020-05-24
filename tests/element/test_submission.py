from gedcom.element.element import Element
from gedcom.element.submission import SubmissionElement
import gedcom.tags


def test_initialization():
    submission_element = SubmissionElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_SUBMISSION, value="")
    assert isinstance(submission_element, Element)
    assert isinstance(submission_element, SubmissionElement)
