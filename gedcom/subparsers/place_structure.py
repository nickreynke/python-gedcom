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
Substructure parser for a `PLACE_STRUCTURE` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_PLACE` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import parse_note_structure


def parse_place_structure(element: Element) -> dict:
    """Parse and extract a `PLACE_STRUCTURE` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_PLACE` tag.
    """
    record = {
        'name': element.get_value(),
        'hierarchy': '',
        'phonetic': [],
        'romanized': [],
        'latitude': '',
        'longitude': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_FORMAT:
            record['hierarchy'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(parse_note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_PHONETIC:
            subrecord = {
                'name': child.get_value(),
                'type': ''
            }
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TYPE:
                    subrecord['type'] = gchild.get_value()
            record['phonetic'].append(subrecord)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ROMANIZED:
            subrecord = {
                'name': child.get_value(),
                'type': ''
            }
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TYPE:
                    subrecord['type'] = gchild.get_value()
            record['romanized'].append(subrecord)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_MAP:
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_LATITUDE:
                    record['latitude'] = gchild.get_value()
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_LONGITUDE:
                    record['longitude'] = gchild.get_value()

    return record
