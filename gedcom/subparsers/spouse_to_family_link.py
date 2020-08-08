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
Substructure parser for a `SPOUSE_TO_FAMILY_LINK` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import parse_note_structure


def parse_spouse_to_family_link(element: Element) -> dict:
    """Parse and extract a `SPOUSE_TO_FAMILY_LINK` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE` tag.
    """
    record = {
        'key_to_family': element.get_value(),
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(parse_note_structure(child))

    return record
