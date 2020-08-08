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
Substructure parser for a `PERSONAL_NAME_STRUCTURE` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_NAME` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.personal_name_pieces import personal_name_pieces


def extract_name(element: Element) -> dict:
    """Parse and extract a `NAME` for a `PERSONAL_NAME_STRUCTURE` structure.

    The `element` should contain one of the name tags:

    `gedcom.tags.GEDCOM_TAG_NAME`

    `gedcom.tags.GEDCOM_TAG_PHONETIC`

    `gedcom.tags.GEDCOM_TAG_ROMANIZED`
    """
    record = {
        'name': '',
        'type': '',
        'pieces': {}
    }
    record['name'] = element.get_value()
    record['pieces'] = personal_name_pieces(element)
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_TYPE:
            record['type'] = child.get_value()
    return record


def personal_name_structure(element: Element) -> dict:
    """Parse and extract a `PERSONAL_NAME_STRUCTURE` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_NAME` tag.
    """
    record = extract_name(element)
    record['phonetic'] = []
    record['romanized'] = []
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_PHONETIC:
            record['phonetic'].append(extract_name(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ROMANIZED:
            record['romanized'].append(extract_name(child))
            continue

    return record
