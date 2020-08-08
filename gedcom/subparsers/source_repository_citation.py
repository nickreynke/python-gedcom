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
Substructure parser for a `SOURCE_REPOSITORY_CITATION` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_REPOSITORY` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import parse_note_structure


def parse_source_repository_citation(element: Element) -> dict:
    """Parse and extract a `SOURCE_REPOSITORY_CITATION` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_REPOSITORY` tag.
    """
    record = {
        'key_to_repository': element.get_value(),
        'call_number': '',
        'media_type': '',
        'notes': []
    }
    if record['key_to_repository'] not in [None, '']:
        if '@' not in record['key_to_repository']:
            record['key_to_repository'] = ''

    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(parse_note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_CALL_NUMBER:
            record['call_number'] = child.get_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_MEDIA:
                    record['media_type'] = gchild.get_value()

    return record
