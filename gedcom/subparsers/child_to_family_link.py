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
Substructure parser for a `CHILD_TO_FAMILY_LINK` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_FAMILY_CHILD` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import note_structure


def child_to_family_link(element: Element) -> dict:
    """Parses and extracts a `CHILD_TO_FAMILY_LINK` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_FAMILY_CHILD` tag.
    """
    record = {
        'key_to_family': element.get_value(),
        'pedigree': '',
        'status': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_PEDIGREE:
            record['pedigree'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_STATUS:
            record['status'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))

    return record
