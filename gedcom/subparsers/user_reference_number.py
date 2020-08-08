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

"""
Parser for a `USER_REFERENCE_NUMBER` structure.

This is anchored by the `gedcom.tags.GEDCOM_TAG_REFERENCE` tag.

This is not a formally documented structure in the standard but it is
a substructure that repeats itself in a number of record types.
"""

import gedcom.tags as tags
from gedcom.element.element import Element


def user_reference_number(element: Element) -> dict:
    """Parse and extract a `USER_REFERENCE_NUMBER` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_REFERENCE` tag.
    """
    record = {
        'reference': element.get_value(),
        'type': ''
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_TYPE:
            record['type'] = child.get_value()

    return record
