# -*- coding: utf-8 -*-

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

"""Virtual GEDCOM root element containing all logical records as children"""

from gedcom.element.element import Element


class RootElement(Element):
    """Virtual GEDCOM root element containing all logical records as children."""

    def __init__(self, level: int = -1, pointer: str = "", tag: str = "ROOT", value: str = "",
                 crlf: str = "\n", multi_line: bool = True):
        super(RootElement, self).__init__(level, pointer, tag, value, crlf, multi_line)
