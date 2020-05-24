from gedcom.element.element import Element
from gedcom.element.repository import RepositoryElement
import gedcom.tags


def test_initialization():
    repository_element = RepositoryElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_REPOSITORY, value="")
    assert isinstance(repository_element, Element)
    assert isinstance(repository_element, RepositoryElement)
