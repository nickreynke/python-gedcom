#  Copyright (C) 2020
#
#  This file is part of the Python GEDCOM Parser.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#  For more, have a look at the GitHub repository at:
#  https://github.com/nickreynke/python-gedcom

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
