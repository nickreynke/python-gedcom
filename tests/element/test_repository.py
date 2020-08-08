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
from gedcom.element.repository import RepositoryElement
import gedcom.tags


def test_initialization():
    repository_element = RepositoryElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_REPOSITORY, value="")
    assert isinstance(repository_element, Element)
    assert isinstance(repository_element, RepositoryElement)
