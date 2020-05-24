from gedcom.element.element import Element
from gedcom.element.note import NoteElement
import gedcom.tags


def test_initialization():
    note_element = NoteElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_NOTE, value="")
    assert isinstance(note_element, Element)
    assert isinstance(note_element, NoteElement)
